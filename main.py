"""
  * In the name of Allah, the merciful, the compassionate.
 * author: Abolfazl Danayi
 * created on 08-09-2026-14h-00m
 * copyright 2026
"""

#!/usr/bin/env python3
"""
ORIB – Optimal Receiver In BCI
PyQt5 GUI that generates a complete Keras/TensorFlow training script
for the BELT architecture.
"""

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QFormLayout, QLabel, QSpinBox, QDoubleSpinBox, QComboBox,
    QLineEdit, QPushButton, QTextEdit, QCheckBox, QFileDialog, QSizePolicy
)
import sys
import os

# ----------------------------------------------------------------------
# Style constants
# ----------------------------------------------------------------------
ACCENT = "#1565C0"
BG = "#F5F5F5"
TEXT = "#212121"
BORDER = "#BDBDBD"

# ----------------------------------------------------------------------
# Helper: create a group box with given title and layout
# ----------------------------------------------------------------------


def make_group(title, layout):
    gb = QGroupBox(title)
    gb.setStyleSheet(f"""
        QGroupBox {{
            border: 1px solid {BORDER};
            border-radius: 5px;
            margin-top: 1.5ex;
            padding-top: 1.5ex;
            font-weight: bold;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }}
    """)
    gb.setLayout(layout)
    gb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
    return gb

# ----------------------------------------------------------------------
# Main window
# ----------------------------------------------------------------------


class ORIBGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ORIB – Optimal Receiver In BCI")
        self.resize(920, 780)   # slightly taller to prevent clipping
        self.setStyleSheet(
            f"background-color: {BG}; color: {TEXT}; font-family: 'Segoe UI', sans-serif; font-size: 10pt;")

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(12, 12, 12, 12)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        main_layout.addWidget(self.tabs)

        # Build tabs
        self.build_tab_data()
        self.build_tab_detector()
        self.build_tab_adversarial()
        self.build_tab_output()

    # ==================================================================
    # TAB 1 – Data & Autoencoder
    # ==================================================================
    def build_tab_data(self):
        tab = QWidget()
        self.tabs.addTab(tab, "Data & Autoencoder")
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)

        # 1.1 Input shape
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

        # 1.2 Compression parameters
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

        # 1.3 Data path
        path_layout = QHBoxLayout()
        self.edit_data_path = QLineEdit()
        btn_browse_data = QPushButton("Browse…")
        btn_browse_data.setStyleSheet(
            f"color: {ACCENT}; border: 1px solid {ACCENT}; padding: 4px 12px; border-radius: 4px;")
        btn_browse_data.clicked.connect(
            lambda: self.browse_folder(self.edit_data_path))
        path_layout.addWidget(QLabel("Data Directory:"))
        path_layout.addWidget(self.edit_data_path)
        path_layout.addWidget(btn_browse_data)
        layout.addWidget(make_group("Data Path", path_layout))

        # 1.4 Training settings
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

    # ==================================================================
    # TAB 2 – Detector
    # ==================================================================
    def build_tab_detector(self):
        tab = QWidget()
        self.tabs.addTab(tab, "Detector")
        layout = QVBoxLayout(tab)
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

        # Hyper-parameters
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
        self.sp_d.setEnabled(False)
        self.sp_f.setEnabled(False)
        self.sp_Nf.setEnabled(False)
        self.sp_Ns.setEnabled(False)
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

    # ==================================================================
    # TAB 3 – Adversarial Demodulators
    # ==================================================================
    def build_tab_adversarial(self):
        tab = QWidget()
        self.tabs.addTab(tab, "Adversarial")
        layout = QVBoxLayout(tab)
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
        da_layout.addRow("LR", self.sp_da_lr)
        da_gb = make_group("Dᵃ (Alpha Demodulator)", da_layout)
        layout.addWidget(da_gb)

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
        db_layout.addRow("LR", self.sp_db_lr)
        db_gb = make_group("Dᵇ (Beta Demodulator)", db_layout)
        layout.addWidget(db_gb)
        layout.addStretch()

    # ==================================================================
    # TAB 4 – Output
    # ==================================================================
    def build_tab_output(self):
        tab = QWidget()
        self.tabs.addTab(tab, "Output")
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)

        # Output path
        out_layout = QHBoxLayout()
        self.edit_output_path = QLineEdit()
        btn_browse_out = QPushButton("Browse…")
        btn_browse_out.setStyleSheet(
            f"color: {ACCENT}; border: 1px solid {ACCENT}; padding: 4px 12px; border-radius: 4px;")
        btn_browse_out.clicked.connect(
            lambda: self.browse_folder(self.edit_output_path))
        out_layout.addWidget(QLabel("Output Directory:"))
        out_layout.addWidget(self.edit_output_path)
        out_layout.addWidget(btn_browse_out)
        layout.addWidget(make_group("Output Path", out_layout))

        # Generate button
        self.btn_generate = QPushButton("Generate Code")
        self.btn_generate.setStyleSheet(
            f"background-color: {ACCENT}; color: white; font-weight: bold; padding: 14px; border-radius: 6px; font-size: 14pt;")
        self.btn_generate.clicked.connect(self.generate_code)
        layout.addWidget(self.btn_generate)

        # Log area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet(
            f"background-color: white; border: 1px solid {BORDER}; border-radius: 4px;")
        layout.addWidget(self.log_area)
        layout.addStretch()

    # ==================================================================
    # Utility
    # ==================================================================
    def browse_folder(self, line_edit):
        path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if path:
            line_edit.setText(path)

    # ==================================================================
    # Code generation (skeleton)
    # ==================================================================
    def generate_code(self):
        out_dir = self.edit_output_path.text().strip()
        if not out_dir:
            self.log_area.append("⚠ Please specify an output directory.")
            return

        script_path = os.path.join(out_dir, "train_belt.py")
        code = self._generate_script_content()
        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(code)
            self.log_area.append(f"✓ Training script saved to: {script_path}")
        except Exception as e:
            self.log_area.append(f"✗ Error writing file: {e}")

    def _generate_script_content(self):
        return f"""#!/usr/bin/env python3
\"\"\"Auto-generated ORIB training script.\"\"\"
import numpy as np
import tensorflow as tf
from tensorflow import keras as K

# ----- Parameters -----
SAMPLES = {self.sp_samples.value()}
CHANNELS = {self.sp_channels.value()}
E1, E2, N = {self.sp_E1.value()}, {self.sp_E2.value()}, {self.sp_N.value()}
AE_EPOCHS = {self.sp_ae_epochs.value()}
AE_BATCH = {self.sp_ae_batch.value()}

DET_WIDTH = "{self.cmb_width.currentText()}"
DET_D, DET_F, DET_NF, DET_NS = {self.sp_d.value()}, {self.sp_f.value()}, {self.sp_Nf.value()}, {self.sp_Ns.value()}
DET_EPOCHS = {self.sp_det_epochs.value()}
DET_LR = {self.sp_det_lr.value()}

DA_LAMBDA_CLS = {self.sp_da_lambda_cls.value()}
DA_LAMBDA_RECON = {self.sp_da_lambda_recon.value()}
DA_LAMBDA_REG = {self.sp_da_lambda_reg.value()}
DA_EPOCHS = {self.sp_da_epochs.value()}
DA_LR = {self.sp_da_lr.value()}

DB_LAMBDA_RECON = {self.sp_db_lambda_recon.value()}
DB_LAMBDA_UNIF = {self.sp_db_lambda_unif.value()}
DB_EPOCHS = {self.sp_db_epochs.value()}
DB_LR = {self.sp_db_lr.value()}

print("Parameters loaded. Replace with full training loop.")
"""


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ORIBGenerator()
    window.show()
    sys.exit(app.exec_())
