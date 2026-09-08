"""
  * بسم الله الرحمن الرحیم
  * اللهم صل علی محمد و آل محمد
 * author: ARC
 * created on 08-09-2026-14h-18m
 * copyright 2026
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class AboutTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel(
            "ORIB – Optimal Receiver In BCI\n\n"
            "Generates training scripts for the BELT architecture.\n"
            "Copyright (c) 2026 Abolfazl Danayi"
        )
        label.setStyleSheet("font-size: 12pt;")
        layout.addWidget(label)
        layout.addStretch()