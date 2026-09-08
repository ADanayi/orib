"""
  * بسم الله الرحمن الرحیم
  * اللهم صل علی محمد و آل محمد
 * author: ARC
 * created on 08-09-2026-16h-21m
 * copyright 2026
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from keras.models import Model


class BaseComponent(ABC):
    """Base class for all BELT components.

    Provides common interface: Keras model, optimizer, training parameters,
    and recompilation.
    """

    def __init__(
        self,
        name: str,
        model: Optional[Model] = None,
        model_width: str = "0.0k",
        optimizer: Optional[Any] = None,
        tr_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._name: str = name
        self._model: Optional[Model] = model
        self._model_width: str = model_width
        self._optimizer: Optional[Any] = optimizer
        self._tr_params: Dict[str, Any] = tr_params or {}

    @property
    def name(self) -> str:
        """Component name."""
        return self._name

    @property
    def model(self) -> Model:
        """The underlying Keras model."""
        if self._model is None:
            raise ValueError(f"Model not built for component '{self.name}'.")
        return self._model

    @model.setter
    def model(self, m: Model) -> None:
        self._model = m

    @property
    def model_width(self) -> str:
        """Model width in 'k' format, e.g., '2.8k'."""
        return self._model_width

    @model_width.setter
    def model_width(self, w: str) -> None:
        self._model_width = w

    @property
    def optimizer(self) -> Optional[Any]:
        """Optimizer used for training."""
        return self._optimizer

    @optimizer.setter
    def optimizer(self, opt: Any) -> None:
        self._optimizer = opt

    @property
    def tr_params(self) -> Dict[str, Any]:
        """Training parameters passed directly to model.fit()."""
        return self._tr_params

    @tr_params.setter
    def tr_params(self, params: Dict[str, Any]) -> None:
        self._tr_params = params

    def recompile(self) -> None:
        """Recompile the model using the current optimizer and loss/metrics."""
        if self._model is not None:
            self._model.compile(
                optimizer=self._optimizer,
                loss=self._loss,
                metrics=self._metrics,
            )

    @property
    @abstractmethod
    def _loss(self) -> Any:
        """Loss function or name to be used in compile."""
        ...

    @property
    @abstractmethod
    def _metrics(self) -> Any:
        """Metric(s) to be used in compile."""
        ...