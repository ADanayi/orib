"""
  * بسم الله الرحمن الرحیم
  * اللهم صل علی محمد و آل محمد
 * author: ARC
 * created on 08-09-2026-14h-17m
 * copyright 2026
"""

from PyQt5.QtWidgets import QGroupBox, QSizePolicy

ACCENT = "#1565C0"
BG = "#F5F5F5"
TEXT = "#212121"
BORDER = "#BDBDBD"


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
        QGroupBox:disabled {{
            color: #888888;
            border: 1px solid #CCCCCC;
        }}
        QGroupBox::title:disabled {{
            color: #888888;
        }}
    """)
    gb.setLayout(layout)
    gb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
    return gb
