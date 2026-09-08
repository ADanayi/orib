from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel,
    QSpinBox, QDoubleSpinBox, QLineEdit, QPushButton, QFileDialog
)
from .utils import make_group, ACCENT


class DataAutoencoderTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # ----------------------------------------------------------
        # Input Shape
        # ----------------------------------------------------------
        shape_layout = QFormLayout()
        self.sp_samples = QSpinBox()
        self.sp_samples.setRange(100, 5000)
        self.sp_samples.setValue(1000)
        self.sp_samples.setToolTip("Number of time samples per EEG trial.")

        self.sp_channels = QSpinBox()
        self.sp_channels.setRange(1, 256)
        self.sp_channels.setValue(3)
        self.sp_channels.setToolTip("Number of EEG channels.")

        shape_layout.addRow("Samples:", self.sp_samples)
        shape_layout.addRow("Channels:", self.sp_channels)
        layout.addWidget(make_group("Input Shape", shape_layout))

        # ----------------------------------------------------------
        # Compression Parameters
        # ----------------------------------------------------------
        comp_layout = QFormLayout()

        # E1 label with subscript
        lbl_E1 = QLabel()
        lbl_E1.setTextFormat(Qt.RichText)
        lbl_E1.setText("E<sub>1</sub> (First stage temporal compression):")

        self.sp_E1 = QSpinBox()
        self.sp_E1.setRange(1, 100)
        self.sp_E1.setValue(5)
        self.sp_E1.setToolTip("First encoder stride factor.")

        # E2 label with subscript
        lbl_E2 = QLabel()
        lbl_E2.setTextFormat(Qt.RichText)
        lbl_E2.setText("E<sub>2</sub> (Second stage temporal compression):")

        self.sp_E2 = QSpinBox()
        self.sp_E2.setRange(1, 100)
        self.sp_E2.setValue(2)
        self.sp_E2.setToolTip("Second encoder stride factor.")

        # N label with subscript
        lbl_N = QLabel()
        lbl_N.setTextFormat(Qt.RichText)
        lbl_N.setText("N (latent dimension):")

        self.sp_N = QSpinBox()
        self.sp_N.setRange(1, 100)
        self.sp_N.setValue(9)
        self.sp_N.setToolTip("Number of latent filters.")

        self.lbl_CR = QLabel("CR = 3.33")
        self.lbl_CR.setStyleSheet("font-weight: bold;")

        comp_layout.addRow(lbl_E1, self.sp_E1)
        comp_layout.addRow(lbl_E2, self.sp_E2)
        comp_layout.addRow(lbl_N, self.sp_N)
        comp_layout.addRow("Compression Ratio:", self.lbl_CR)

        for sp in (self.sp_E1, self.sp_E2, self.sp_N, self.sp_channels):
            sp.valueChanged.connect(self.update_CR)

        layout.addWidget(make_group("Compression Parameters", comp_layout))

        # ----------------------------------------------------------
        # Data Path
        # ----------------------------------------------------------
        path_layout = QHBoxLayout()
        self.edit_data_path = QLineEdit()
        self.edit_data_path.setPlaceholderText("Select folder containing dataset...")
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

        # ----------------------------------------------------------
        # Training Settings
        # ----------------------------------------------------------
        train_layout = QFormLayout()

        self.sp_ae_epochs = QSpinBox()
        self.sp_ae_epochs.setRange(1, 10000)
        self.sp_ae_epochs.setValue(100)
        train_layout.addRow("Epochs:", self.sp_ae_epochs)

        self.sp_ae_batch = QSpinBox()
        self.sp_ae_batch.setRange(1, 4096)
        self.sp_ae_batch.setValue(64)
        train_layout.addRow("Batch Size:", self.sp_ae_batch)

        self.sp_ae_lr = QDoubleSpinBox()
        self.sp_ae_lr.setRange(1e-6, 1e-1)
        self.sp_ae_lr.setDecimals(6)
        self.sp_ae_lr.setSingleStep(1e-4)
        self.sp_ae_lr.setValue(1e-4)
        train_layout.addRow("Learning Rate:", self.sp_ae_lr)

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