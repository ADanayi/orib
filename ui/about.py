"""
  * بسم الله الرحمن الرحیم
  * اللهم صل علی محمد و آل محمد
 * author: ARC
 * created on 08-09-2026-14h-18m
 * copyright 2026
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QFrame
from PyQt5.QtCore import Qt


class AboutTab(QWidget):
    VERSION = "v0.1.1"
    PLOS_DOI = "10.1371/journal.pone.0354976"
    PLOS_URL = "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0354976"
    GITHUB_URL = "https://github.com/adanayi/orib"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.build_ui()

    def build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # Title and description
        title_label = QLabel("ORIB – Optimal Receiver In BCI")
        title_label.setStyleSheet("font-size: 16pt; font-weight: bold;")
        main_layout.addWidget(title_label)

        desc_label = QLabel(
            "Generates training scripts for the BELT architecture.\n"
            "Copyright (c) 2026 Abolfazl Danayi"
        )
        main_layout.addWidget(desc_label)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        # Version
        version_label = QLabel(f"Version: <b>{self.VERSION}</b>")
        version_label.setTextFormat(Qt.RichText)
        main_layout.addWidget(version_label)

        # Paper reference with clickable DOI
        paper_label = QLabel()
        paper_label.setTextFormat(Qt.RichText)
        paper_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        paper_label.setOpenExternalLinks(False)
        paper_label.setText(
            f'Paper: <a href="{self.PLOS_URL}" style="color: #1565C0;">'
            f'Improved Motor Imagery BCI Performance via Task-Unaware Compression in the BELT Bayesian Edge-Cloud Architecture</a><br>'
            f'DOI: <a href="{self.PLOS_URL}" style="color: #1565C0;">{self.PLOS_DOI}</a>'
        )
        paper_label.linkActivated.connect(self.open_link)
        main_layout.addWidget(paper_label)

        # GitHub link
        github_label = QLabel()
        github_label.setTextFormat(Qt.RichText)
        github_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        github_label.setOpenExternalLinks(False)
        github_label.setText(
            f'GitHub: <a href="{self.GITHUB_URL}" style="color: #1565C0;">{self.GITHUB_URL}</a>'
        )
        github_label.linkActivated.connect(self.open_link)
        main_layout.addWidget(github_label)

        main_layout.addStretch()

    @staticmethod
    def open_link(url):
        QDesktopServices.openUrl(QUrl(url))
