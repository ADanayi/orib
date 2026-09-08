"""
  * بسم الله الرحمن الرحیم
  * اللهم صل علی محمد و آل محمد
 * author: ARC
 * created on 08-09-2026-14h-18m
 * copyright 2026
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QDoubleSpinBox, QSpinBox
)
from .utils import make_group


class AdversarialTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # D^a group
        da_layout = QFormLayout()
        self.sp_da_lambda_cls = QDoubleSpinBox()
        self.sp_da_lambda_cls.setValue(1.0)
        self.sp_da_lambda_cls.setRange(0, 100)
        self.sp_da_lambda_cls.setDecimals(2)

        self.sp_da_lambda_recon = QDoubleSpinBox()
        self.sp_da_lambda_recon.setValue(0.1)
        self.sp_da_lambda_recon.setRange(0, 100)
        self.sp_da_lambda_recon.setDecimals(2)

        self.sp_da_lambda_reg = QDoubleSpinBox()
        self.sp_da_lambda_reg.setValue(1e-5)
        self.sp_da_lambda_reg.setRange(0, 1)
        self.sp_da_lambda_reg.setDecimals(6)
        self.sp_da_lambda_reg.setSingleStep(1e-5)

        self.sp_da_epochs = QSpinBox()
        self.sp_da_epochs.setRange(1, 1000)
        self.sp_da_epochs.setValue(100)

        self.sp_da_lr = QDoubleSpinBox()
        self.sp_da_lr.setRange(1e-6, 1e-1)
        self.sp_da_lr.setDecimals(6)
        self.sp_da_lr.setSingleStep(1e-4)
        self.sp_da_lr.setValue(1e-4)

        da_layout.addRow("λ_cls", self.sp_da_lambda_cls)
        da_layout.addRow("λ_recon", self.sp_da_lambda_recon)
        da_layout.addRow("λ_reg", self.sp_da_lambda_reg)
        da_layout.addRow("Epochs", self.sp_da_epochs)
        da_layout.addRow("Learning Rate", self.sp_da_lr)

        layout.addWidget(make_group("Dᵃ (Alpha Demodulator)", da_layout))

        # D^b group
        db_layout = QFormLayout()
        self.sp_db_lambda_recon = QDoubleSpinBox()
        self.sp_db_lambda_recon.setValue(1.0)
        self.sp_db_lambda_recon.setRange(0, 100)
        self.sp_db_lambda_recon.setDecimals(2)

        self.sp_db_lambda_unif = QDoubleSpinBox()
        self.sp_db_lambda_unif.setValue(1.0)
        self.sp_db_lambda_unif.setRange(0, 100)
        self.sp_db_lambda_unif.setDecimals(2)

        self.sp_db_epochs = QSpinBox()
        self.sp_db_epochs.setRange(1, 1000)
        self.sp_db_epochs.setValue(40)

        self.sp_db_lr = QDoubleSpinBox()
        self.sp_db_lr.setRange(1e-6, 1e-1)
        self.sp_db_lr.setDecimals(6)
        self.sp_db_lr.setSingleStep(1e-4)
        self.sp_db_lr.setValue(1e-4)

        db_layout.addRow("λ_recon", self.sp_db_lambda_recon)
        db_layout.addRow("λ_unif", self.sp_db_lambda_unif)
        db_layout.addRow("Epochs", self.sp_db_epochs)
        db_layout.addRow("Learning Rate", self.sp_db_lr)

        layout.addWidget(make_group("Dᵇ (Beta Demodulator)", db_layout))
        layout.addStretch()