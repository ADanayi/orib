"""
  * بسم الله الرحمن الرحیم
  * اللهم صل علی محمد و آل محمد
 * author: ARC
 * created on 08-09-2026-14h-18m
 * copyright 2026
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QFileDialog
)
from .utils import make_group, ACCENT, BORDER


class OutputTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Output path
        out_layout = QHBoxLayout()
        self.edit_output_path = QLineEdit()
        btn_browse_out = QPushButton("Browse…")
        btn_browse_out.setStyleSheet(
            f"color: {ACCENT}; border: 1px solid {ACCENT}; "
            "padding: 4px 12px; border-radius: 4px;"
        )
        btn_browse_out.clicked.connect(
            lambda: self.browse_folder(self.edit_output_path)
        )
        out_layout.addWidget(QLabel("Output Directory:"))
        out_layout.addWidget(self.edit_output_path)
        out_layout.addWidget(btn_browse_out)
        layout.addWidget(make_group("Output Path", out_layout))

        # Generate button
        self.btn_generate = QPushButton("Generate Code")
        self.btn_generate.setStyleSheet(
            f"background-color: {ACCENT}; color: white; font-weight: bold; "
            "padding: 14px; border-radius: 6px; font-size: 14pt;"
        )
        layout.addWidget(self.btn_generate)

        # Log area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet(
            f"background-color: white; border: 1px solid {BORDER}; "
            "border-radius: 4px;"
        )
        layout.addWidget(self.log_area)
        layout.addStretch()

    def browse_folder(self, line_edit):
        path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if path:
            line_edit.setText(path)