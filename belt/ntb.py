"""
  * بسم الله الرحمن الرحیم
  * اللهم صل علی محمد و آل محمد
 * author: ARC
 * created on 08-09-2026-16h-21m
 * copyright 2026
"""

# belt/ntb.py
import tensorflow as tf
from tensorflow.keras.layers import Layer
from keras.saving import register_keras_serializable


@register_keras_serializable()
class NTBSquareLayer(Layer):
    def call(self, x):
        return tf.square(x)


@register_keras_serializable()
class NTBLogLayer(Layer):
    def call(self, x):
        return tf.math.log(x + 1e-8)


def create_ntb(ntb_factor: int = 26):
    """Return a list of layers implementing the NTB block."""
    window = int(ntb_factor * 20 / 13)
    stride = ntb_factor
    return [
        NTBSquareLayer(name="NTB-square"),
        tf.keras.layers.AveragePooling1D(window, strides=stride, name="NTB-avg"),
        NTBLogLayer(name="NTB-log"),
    ]