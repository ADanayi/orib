"""
  * بسم الله الرحمن الرحیم
  * اللهم صل علی محمد و آل محمد
 * author: ARC
 * created on 08-09-2026-14h-18m
 * copyright 2026
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox,
    QComboBox, QCheckBox
)
from .utils import make_group


class DetectorTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Preset width
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("Model Width:"))
        self.cmb_width = QComboBox()
        self.cmb_width.addItems(["2.8k", "1k", "0.4k"])
        self.cmb_width.setCurrentIndex(1)
        self.cmb_width.currentIndexChanged.connect(self.on_preset_changed)
        preset_layout.addWidget(self.cmb_width)

        self.chk_override = QCheckBox("Override")
        self.chk_override.toggled.connect(self.on_override_toggled)
        preset_layout.addWidget(self.chk_override)
        preset_layout.addStretch()
        layout.addWidget(make_group("Preset Width", preset_layout))

        # Hyper‑parameters
        hp_layout = QHBoxLayout()
        hp_layout.addWidget(QLabel("d:"))
        self.sp_d = QSpinBox()
        self.sp_d.setRange(1, 100)
        self.sp_d.setValue(2)
        hp_layout.addWidget(QLabel("f:"))
        self.sp_f = QSpinBox()
        self.sp_f.setRange(1, 1000)
        self.sp_f.setValue(52)
        hp_layout.addWidget(QLabel("Nf:"))
        self.sp_Nf = QSpinBox()
        self.sp_Nf.setRange(1, 100)
        self.sp_Nf.setValue(2)
        hp_layout.addWidget(QLabel("Ns:"))
        self.sp_Ns = QSpinBox()
        self.sp_Ns.setRange(1, 100)
        self.sp_Ns.setValue(10)

        # Disabled until override is checked
        for sp in (self.sp_d, self.sp_f, self.sp_Nf, self.sp_Ns):
            sp.setEnabled(False)

        hp_layout.addStretch()
        layout.addWidget(make_group("Hyper‑Parameters", hp_layout))

        # Training
        train_layout = QHBoxLayout()
        train_layout.addWidget(QLabel("Epochs:"))
        self.sp_det_epochs = QSpinBox()
        self.sp_det_epochs.setRange(1, 10000)
        self.sp_det_epochs.setValue(100)
        train_layout.addWidget(QLabel("LR:"))
        self.sp_det_lr = QDoubleSpinBox()
        self.sp_det_lr.setRange(1e-6, 1e-1)
        self.sp_det_lr.setDecimals(6)
        self.sp_det_lr.setSingleStep(1e-4)
        self.sp_det_lr.setValue(1e-4)
        train_layout.addStretch()
        layout.addWidget(make_group("Training Settings", train_layout))
        layout.addStretch()

    def on_preset_changed(self, idx):
        presets = {
            0: (2, 26, 3, 16),
            1: (2, 52, 2, 10),
            2: (4, 104, 2, 8)
        }
        d, f, nf, ns = presets[idx]
        self.sp_d.setValue(d)
        self.sp_f.setValue(f)
        self.sp_Nf.setValue(nf)
        self.sp_Ns.setValue(ns)

    def on_override_toggled(self, checked):
        for sp in (self.sp_d, self.sp_f, self.sp_Nf, self.sp_Ns):
            sp.setEnabled(checked)