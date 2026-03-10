import sys
import cv2
import qrcode
import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QPushButton,
    QLineEdit, QMessageBox,QFileDialog
)

class QRCodeGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Code Generator")
        
        # Widgets
        self.text = QLineEdit(self)
        self.btnSave = QPushButton("Generate and Save QR", self)

        # Layout
        self.layoutWin = QFormLayout(self)
        self.layoutWin.addRow("Enter Text for the QR Code:", self.text)
        self.layoutWin.addRow(self.btnSave)

        # Connect button to handler
        self.btnSave.clicked.connect(self.generate_qrcode)

    def generate_qrcode(self):
        data = self.text.text().strip()
        if not data:
            QMessageBox.warning(self, "Warning", "Please enter some text.")
            return

        # Generate QR using qrcode
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4
        )
        qr.add_data(data)
        qr.make(fit=True)
        img_pil = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

        # Save using OpenCV
        filename, _ = QFileDialog.getSaveFileName(self, "Save As", "QRCodes_images/", "PNG Files (*.png)")
        if filename:
            cv2.imwrite(filename, img_cv)
            QMessageBox.information(self, "Saved", f"QR Code saved as:\n{filename}")


