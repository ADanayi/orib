"""
  * بسم الله الرحمن الرحیم
  * اللهم صل علی محمد و آل محمد
 * author: ARC
 * created on 08-09-2026-14h-17m
 * copyright 2026
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QLineEdit,
    QPushButton, QFileDialog
)
from .utils import make_group, ACCENT


class DataAutoencoderTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Input shape
        shape_layout = QHBoxLayout()
        shape_layout.addWidget(QLabel("Input Shape (samples, channels):"))
        self.sp_samples = QSpinBox()
        self.sp_samples.setRange(100, 5000)
        self.sp_samples.setValue(1000)
        self.sp_channels = QSpinBox()
        self.sp_channels.setRange(1, 256)
        self.sp_channels.setValue(3)
        shape_layout.addWidget(self.sp_samples)
        shape_layout.addWidget(self.sp_channels)
        shape_layout.addStretch()
        layout.addWidget(make_group("Input Shape", shape_layout))

        # Compression parameters
        comp_layout = QHBoxLayout()
        comp_layout.addWidget(QLabel("E₁:"))
        self.sp_E1 = QSpinBox()
        self.sp_E1.setRange(1, 100)
        self.sp_E1.setValue(5)
        comp_layout.addWidget(QLabel("E₂:"))
        self.sp_E2 = QSpinBox()
        self.sp_E2.setRange(1, 100)
        self.sp_E2.setValue(2)
        comp_layout.addWidget(QLabel("N:"))
        self.sp_N = QSpinBox()
        self.sp_N.setRange(1, 100)
        self.sp_N.setValue(9)
        comp_layout.addStretch()
        self.lbl_CR = QLabel("CR = 3.33")
        comp_layout.addWidget(self.lbl_CR)

        for sp in (self.sp_E1, self.sp_E2, self.sp_N, self.sp_channels):
            sp.valueChanged.connect(self.update_CR)

        layout.addWidget(make_group("Compression Parameters", comp_layout))

        # Data path
        path_layout = QHBoxLayout()
        self.edit_data_path = QLineEdit()
        btn_browse_data = QPushButton("Browse…")
        btn_browse_data.setStyleSheet(
            f"color: {ACCENT}; border: 1px solid {ACCENT}; "
            "padding: 4px 12px; border-radius: 4px;"
        )
        btn_browse_data.clicked.connect(
            lambda: self.browse_folder(self.edit_data_path)
        )
        path_layout.addWidget(QLabel("Data Directory:"))
        path_layout.addWidget(self.edit_data_path)
        path_layout.addWidget(btn_browse_data)
        layout.addWidget(make_group("Data Path", path_layout))

        # Training settings
        train_layout = QHBoxLayout()
        train_layout.addWidget(QLabel("Epochs:"))
        self.sp_ae_epochs = QSpinBox()
        self.sp_ae_epochs.setRange(1, 10000)
        self.sp_ae_epochs.setValue(100)
        train_layout.addWidget(QLabel("Batch Size:"))
        self.sp_ae_batch = QSpinBox()
        self.sp_ae_batch.setRange(1, 4096)
        self.sp_ae_batch.setValue(64)
        train_layout.addStretch()
        layout.addWidget(make_group("Training Settings", train_layout))
        layout.addStretch()

    def update_CR(self):
        C = self.sp_channels.value()
        E1 = self.sp_E1.value()
        E2 = self.sp_E2.value()
        N = self.sp_N.value()
        cr = (C * E1 * E2) / N if N else 0
        self.lbl_CR.setText(f"CR = {cr:.2f}")

    def browse_folder(self, line_edit):
        path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if path:
            line_edit.setText(path)