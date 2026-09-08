"""
  * بسم الله الرحمن الرحیم
  * اللهم صل علی محمد و آل محمد
 * author: ARC
 * created on 08-09-2026-14h-19m
 * copyright 2026
"""

import os
from pathlib import Path

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget
)

from .dataAutoencoder import DataAutoencoderTab
from .detector import DetectorTab
from .adversarial import AdversarialTab
from .output import OutputTab
from .about import AboutTab
from .utils import BG, TEXT

# Assuming the generator is in orib/gen/code_generator.py
from gen import CodeGenerator


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

        # Collect parameters from UI tabs
        params = self._collect_parameters()

        # Path to the BELT component directory
        belt_dir = Path(__file__).parent.parent / "belt"
        generator = CodeGenerator(belt_dir)

        # Optional NTB file
        ntb_file = self.detector_tab.edit_ntb_path.text().strip()
        ntb_source = ntb_file if ntb_file else None

        try:
            generator.generate(
                output_dir=out_dir,
                parameters=params,
                ntb_source=ntb_source
            )
            self.output_tab.log_area.append(
                f"✓ Project generated successfully in: {out_dir}"
            )
        except Exception as e:
            self.output_tab.log_area.append(f"✗ Error generating project: {e}")

    def _collect_parameters(self):
        """Collect all necessary parameters from UI tabs."""
        return {
            # Detector hyperparameters
            "downscale_factor": self.detector_tab.sp_d.value(),
            "filters_per_channel": self.detector_tab.sp_Nf.value(),
            "spatial_filters": self.detector_tab.sp_Ns.value(),
            "ntb_factor": self.detector_tab.sp_f.value(),
            # Input shape
            "input_shape_samples": self.data_tab.sp_samples.value(),
            "input_shape_channels": self.data_tab.sp_channels.value(),
            "num_classes": 2,
            # Detector training
            "learning_rate": self.detector_tab.sp_det_lr.value(),
            # Autoencoder parameters (for future use)
            "E1": self.data_tab.sp_E1.value(),
            "E2": self.data_tab.sp_E2.value(),
            "N": self.data_tab.sp_N.value(),
            "ae_epochs": self.data_tab.sp_ae_epochs.value(),
            "ae_batch": self.data_tab.sp_ae_batch.value(),
            "ae_lr": self.data_tab.sp_ae_lr.value(),
            # Adversarial parameters (for future use)
            "da_lambda_cls": self.adversarial_tab.sp_da_lambda_cls.value(),
            "da_lambda_recon": self.adversarial_tab.sp_da_lambda_recon.value(),
            "da_lambda_reg": self.adversarial_tab.sp_da_lambda_reg.value(),
            "da_epochs": self.adversarial_tab.sp_da_epochs.value(),
            "da_lr": self.adversarial_tab.sp_da_lr.value(),
            "db_lambda_recon": self.adversarial_tab.sp_db_lambda_recon.value(),
            "db_lambda_unif": self.adversarial_tab.sp_db_lambda_unif.value(),
            "db_epochs": self.adversarial_tab.sp_db_epochs.value(),
            "db_lr": self.adversarial_tab.sp_db_lr.value(),
        }