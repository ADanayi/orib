#!/usr/bin/env python3

"""
  * بسم الله الرحمن الرحیم
  * اللهم صل علی محمد و آل محمد
 * author: ARC
 * created on 08-09-2026-14h-19m
 * copyright 2026
"""

"""
ORIB – Optimal Receiver In BCI
PyQt5 GUI that generates a complete Keras/TensorFlow training script
for the BELT architecture.
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.skeleton import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())