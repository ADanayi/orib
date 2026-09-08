from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel,
    QSpinBox, QDoubleSpinBox, QComboBox, QLineEdit, QPushButton,
    QFileDialog
)
from .utils import make_group, ACCENT


class DetectorTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # ----------------------------------------------------------
        # Model Width
        # ----------------------------------------------------------
        width_layout = QFormLayout()

        self.cmb_width = QComboBox()
        self.cmb_width.addItems(["2.8k", "1k", "0.4k", "Custom"])
        self.cmb_width.setCurrentIndex(1)
        self.cmb_width.currentIndexChanged.connect(self.on_preset_changed)

        width_layout.addRow("Model Width:", self.cmb_width)
        layout.addWidget(make_group("Preset Width", width_layout))

        # ----------------------------------------------------------
        # Hyper‑Parameters
        # ----------------------------------------------------------
        hp_layout = QFormLayout()

        # d label
        lbl_d = QLabel()
        lbl_d.setTextFormat(Qt.RichText)
        lbl_d.setText("d (down‑sampling factor):")

        self.sp_d = QSpinBox()
        self.sp_d.setRange(1, 100)
        self.sp_d.setValue(2)
        self.sp_d.setToolTip(
            "Temporal down‑sampling factor applied before LTI filters.")

        # f label
        lbl_f = QLabel()
        lbl_f.setTextFormat(Qt.RichText)
        lbl_f.setText("f (NTB stride factor):")

        self.sp_f = QSpinBox()
        self.sp_f.setRange(1, 1000)
        self.sp_f.setValue(52)
        self.sp_f.setToolTip("Stride factor for the NTB pooling window.")

        # Nf label
        lbl_Nf = QLabel()
        lbl_Nf.setTextFormat(Qt.RichText)
        lbl_Nf.setText("N<sub>f</sub> (LTI filters per channel):")

        self.sp_Nf = QSpinBox()
        self.sp_Nf.setRange(1, 100)
        self.sp_Nf.setValue(2)
        self.sp_Nf.setToolTip(
            "Number of LTI filters applied per input channel.")

        # Ns label
        lbl_Ns = QLabel()
        lbl_Ns.setTextFormat(Qt.RichText)
        lbl_Ns.setText("N<sub>s</sub> (spatial filters):")

        self.sp_Ns = QSpinBox()
        self.sp_Ns.setRange(1, 100)
        self.sp_Ns.setValue(10)
        self.sp_Ns.setToolTip("Number of spatial filters after LTI filtering.")

        hp_layout.addRow(lbl_d, self.sp_d)
        hp_layout.addRow(lbl_f, self.sp_f)
        hp_layout.addRow(lbl_Nf, self.sp_Nf)
        hp_layout.addRow(lbl_Ns, self.sp_Ns)

        # Initially disabled because preset is active
        for sp in (self.sp_d, self.sp_f, self.sp_Nf, self.sp_Ns):
            sp.setEnabled(False)

        self.hp_group = make_group("Hyper‑Parameters", hp_layout)
        layout.addWidget(self.hp_group)
        self.set_hyperparams_enabled(False)

        # ----------------------------------------------------------
        # NTB File Path
        # ----------------------------------------------------------
        ntb_layout = QHBoxLayout()
        self.edit_ntb_path = QLineEdit()
        self.edit_ntb_path.setPlaceholderText(
            "Select Python file containing create_ntb() function..."
        )
        btn_browse_ntb = QPushButton("Browse…")
        btn_browse_ntb.setStyleSheet(
            f"color: {ACCENT}; border: 1px solid {ACCENT}; "
            "padding: 4px 12px; border-radius: 4px;"
        )
        btn_browse_ntb.clicked.connect(self.browse_ntb_file)

        ntb_layout.addWidget(QLabel("NTB File:"))
        ntb_layout.addWidget(self.edit_ntb_path)
        ntb_layout.addWidget(btn_browse_ntb)
        layout.addWidget(make_group("Network Tuning Block (NTB)", ntb_layout))

        # ----------------------------------------------------------
        # Training Settings
        # ----------------------------------------------------------
        train_layout = QFormLayout()

        self.sp_det_epochs = QSpinBox()
        self.sp_det_epochs.setRange(1, 10000)
        self.sp_det_epochs.setValue(100)
        train_layout.addRow("Epochs:", self.sp_det_epochs)

        self.sp_det_batch = QSpinBox()
        self.sp_det_batch.setRange(1, 4096)
        self.sp_det_batch.setValue(64)
        train_layout.addRow("Batch Size:", self.sp_det_batch)

        self.sp_det_lr = QDoubleSpinBox()
        self.sp_det_lr.setRange(1e-6, 1e-1)
        self.sp_det_lr.setDecimals(6)
        self.sp_det_lr.setSingleStep(1e-4)
        self.sp_det_lr.setValue(1e-4)
        train_layout.addRow("Learning Rate:", self.sp_det_lr)

        layout.addWidget(make_group("Training Settings", train_layout))
        layout.addStretch()

    def set_hyperparams_enabled(self, enabled):
        self.hp_group.setEnabled(enabled)

        for child in self.hp_group.findChildren(QWidget):
            child.setEnabled(enabled)
            if enabled:
                child.setStyleSheet("")
            else:
                child.setStyleSheet(
                    "color: #888888; background-color: #F0F0F0;"
                )

    def on_preset_changed(self, idx):
        presets = {
            0: (2, 26, 3, 16),
            1: (2, 52, 2, 10),
            2: (4, 104, 2, 8)
        }
        if idx < 3:
            # Preset selected: set values and disable the whole group
            d, f, nf, ns = presets[idx]
            self.sp_d.setValue(d)
            self.sp_f.setValue(f)
            self.sp_Nf.setValue(nf)
            self.sp_Ns.setValue(ns)
            self.set_hyperparams_enabled(False)
        else:
            self.set_hyperparams_enabled(True)

    def browse_ntb_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select NTB Python File",
            "",
            "Python Files (*.py)"
        )
        if path:
            self.edit_ntb_path.setText(path)
