"""
  * بسم الله الرحمن الرحیم
  * اللهم صل علی محمد و آل محمد
 * author: ARC
 * created on 08-09-2026-14h-19m
 * copyright 2026
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget
)
from .dataAutoencoder import DataAutoencoderTab
from .detector import DetectorTab
from .adversarial import AdversarialTab
from .output import OutputTab
from .about import AboutTab
from .utils import BG, TEXT


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ORIB – Optimal Receiver In BCI")
        self.resize(920, 780)
        self.setStyleSheet(
            f"background-color: {BG}; color: {TEXT}; "
            "font-family: 'Segoe UI', sans-serif; font-size: 10pt;"
        )

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(12, 12, 12, 12)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        main_layout.addWidget(self.tabs)

        # Create tab instances
        self.data_tab = DataAutoencoderTab()
        self.detector_tab = DetectorTab()
        self.adversarial_tab = AdversarialTab()
        self.output_tab = OutputTab()
        self.about_tab = AboutTab()

        # Add tabs
        self.tabs.addTab(self.data_tab, "Data & Autoencoder")
        self.tabs.addTab(self.detector_tab, "Detector")
        self.tabs.addTab(self.adversarial_tab, "Adversarial")
        self.tabs.addTab(self.output_tab, "Output")
        self.tabs.addTab(self.about_tab, "About")

        # Connect generation button
        self.output_tab.btn_generate.clicked.connect(self.generate_code)

    def generate_code(self):
        out_dir = self.output_tab.edit_output_path.text().strip()
        if not out_dir:
            self.output_tab.log_area.append("⚠ Please specify an output directory.")
            return

        script_path = os.path.join(out_dir, "train_belt.py")
        code = self._generate_script_content()
        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(code)
            self.output_tab.log_area.append(f"✓ Training script saved to: {script_path}")
        except Exception as e:
            self.output_tab.log_area.append(f"✗ Error writing file: {e}")

    def _generate_script_content(self):
        # Stub – to be expanded later
        return f"""#!/usr/bin/env python3
\"\"\"Auto-generated ORIB training script.\"\"\"
import numpy as np
import tensorflow as tf
from tensorflow import keras as K

# ----- Parameters -----
SAMPLES = {self.data_tab.sp_samples.value()}
CHANNELS = {self.data_tab.sp_channels.value()}
E1, E2, N = {self.data_tab.sp_E1.value()}, {self.data_tab.sp_E2.value()}, {self.data_tab.sp_N.value()}
AE_EPOCHS = {self.data_tab.sp_ae_epochs.value()}
AE_BATCH = {self.data_tab.sp_ae_batch.value()}

DET_WIDTH = "{self.detector_tab.cmb_width.currentText()}"
DET_D, DET_F, DET_NF, DET_NS = {self.detector_tab.sp_d.value()}, {self.detector_tab.sp_f.value()}, {self.detector_tab.sp_Nf.value()}, {self.detector_tab.sp_Ns.value()}
DET_EPOCHS = {self.detector_tab.sp_det_epochs.value()}
DET_LR = {self.detector_tab.sp_det_lr.value()}

DA_LAMBDA_CLS = {self.adversarial_tab.sp_da_lambda_cls.value()}
DA_LAMBDA_RECON = {self.adversarial_tab.sp_da_lambda_recon.value()}
DA_LAMBDA_REG = {self.adversarial_tab.sp_da_lambda_reg.value()}
DA_EPOCHS = {self.adversarial_tab.sp_da_epochs.value()}
DA_LR = {self.adversarial_tab.sp_da_lr.value()}

DB_LAMBDA_RECON = {self.adversarial_tab.sp_db_lambda_recon.value()}
DB_LAMBDA_UNIF = {self.adversarial_tab.sp_db_lambda_unif.value()}
DB_EPOCHS = {self.adversarial_tab.sp_db_epochs.value()}
DB_LR = {self.adversarial_tab.sp_db_lr.value()}

print("Parameters loaded. Replace with full training loop.")
"""