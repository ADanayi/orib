"""
  * بسم الله الرحمن الرحیم
  * اللهم صل علی محمد و آل محمد
 * author: ARC
 * created on 08-09-2026-16h-23m
 * copyright 2026
"""

# belt/detector.py
import tensorflow as tf
from tensorflow.keras import layers as KL
from tensorflow.keras import models as KM
from tensorflow.keras.constraints import max_norm

from .base import BaseComponent
from . import ntb as default_ntb


class Detector(BaseComponent):
    """
    Detector component of BELT.
    """

    def __init__(self, downscale_factor=2, ntb_factor=26,
                 filters_per_channel=3, spatial_filters=16,
                 input_shape=(1000, 3), num_classes=2,
                 learning_rate=1e-4, ntb_file=None, **kwargs):
        super().__init__(name="detector", **kwargs)

        self.downscale_factor = downscale_factor
        self.ntb_factor = ntb_factor
        self.filters_per_channel = filters_per_channel
        self.spatial_filters = spatial_filters
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.learning_rate = learning_rate

        self._optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        self._build_model(ntb_file)

    def _build_model(self, ntb_file=None):
        if ntb_file:
            import importlib.util
            spec = importlib.util.spec_from_file_location("user_ntb", ntb_file)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            ntb_layers = mod.create_ntb(self.ntb_factor)
        else:
            ntb_layers = default_ntb.create_ntb(self.ntb_factor)

        model = KM.Sequential(name="core")
        model.add(KL.Input(shape=self.input_shape))

        # Downscaler
        model.add(KL.Conv1D(3, 25, groups=3, use_bias=False, activation="linear", padding="same"))
        model.add(KL.AveragePooling1D(self.downscale_factor))

        # LTI band‑pass filters
        model.add(KL.Conv1D(
            3 * self.filters_per_channel,
            kernel_size=25,
            groups=3,
            use_bias=False,
            activation="linear",
            padding="same",
            name="LTI-BP-Filts",
        ))

        # Spatial filters
        model.add(KL.Conv1D(
            self.spatial_filters,
            kernel_size=1,
            strides=1,
            use_bias=False,
            activation="linear",
            padding="valid",
            name="LTI-Spatial-Filts",
        ))
        model.add(KL.BatchNormalization())

        # NTB block
        for layer in ntb_layers:
            model.add(layer)

        model.add(KL.Flatten())
        model.add(KL.BatchNormalization())

        # Classifier
        model.add(KL.Dense(4, activation="relu",
                           kernel_constraint=max_norm(0.25), name="Cfier-l1"))
        model.add(KL.Dropout(0.5))
        model.add(KL.Dense(self.num_classes, activation="sigmoid", name="Cfier-lo"))

        self.model = model

        # Compute model width in "k" format
        num_params = self.model.count_params()
        self.model_width = f"{num_params/1000:.1f}k"

    @property
    def _loss(self):
        return "binary_crossentropy" if self.num_classes == 2 else "categorical_crossentropy"

    @property
    def _metrics(self):
        return ["accuracy"]