from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel,QHBoxLayout
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer, pyqtSignal
import cv2
from PyQt6.QtCore import Qt

class CameraView(QWidget):
    read = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.version="E-Register 1.2"
        print("CameraView initialized")  # DEBUG
        self.qr_detector = cv2.QRCodeDetector()  # QR code detector
        self.lay = QVBoxLayout()
        self.label1 = QLabel("")
        self.label1.setObjectName("DisplayName")
        self.label2 = QLabel()
        self.label3=QLabel()
        pixmap = QPixmap("assets/school_Logo.png")
        scaled = pixmap.scaled(self.label3.size(),Qt.AspectRatioMode.KeepAspectRatioByExpanding,
    Qt.TransformationMode.SmoothTransformation)
        scaled.scaledToWidth(900)
        self.label3.setPixmap(scaled)
        self.label3.setScaledContents(True)
        self.layLabels=QHBoxLayout()
     
       # self.label2.setFixedSize(500, 500)
        self.label3.setFixedSize(100,100)

        self.layLabels.addWidget(self.label3)
        self.layLabels.addWidget(self.label1)
        self.lay.addLayout(self.layLabels)
        self.lay.addWidget(self.label2)

        self.setLayout(self.lay)

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.label1.setText("Camera not found")
            return

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Capture every 30ms

        self.setMinimumSize(900, 500)
        self.setWindowTitle("Camera Feed")
        self.show()

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to read from camera")
            return

        # QR Code detection
        data, bbox, qrImage = self.qr_detector.detectAndDecode(frame)
        # If QR code is detected
        if data and bbox is not None:
            # Check that the bounding box has valid points
            if len(bbox) > 0 and len(bbox[0]) > 0:
                contour_area = cv2.contourArea(bbox.astype(int))  # Calculate area of QR code contour
                if contour_area > 0:
                    self.label1.setText(f"{data}")
                    self.read.emit(data)  # Emit the detected QR code data
                else:
                    #self.label1.setText("Invalid QR code detected.")  # Invalid QR code
                    return
            else:
                #self.label1.setText("Invalid QR code points.")
                return
        else:
            pass
            

        # Draw the bounding box if QR code detected
        if bbox is not None and len(bbox) > 0:
            bbox = bbox.astype(int)
            for i in range(len(bbox[0])):
                pt1 = tuple(bbox[0][i])
                pt2 = tuple(bbox[0][(i + 1) % len(bbox[0])])
                cv2.line(frame, pt1, pt2, (0, 255, 0), 2)  # Draw green bounding box

        # Convert to RGB for Qt display
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pix = QPixmap.fromImage(qt_image)

        self.label2.setPixmap(pix)  # Display on label2

    def stop_camera(self):
        if self.cap.isOpened():
            self.cap.release()  # Release the camera
        self.timer.stop()  # Stop the timer
        self.label1.setText("Camera stopped.")
        self.label2.clear()  # Clear the display

    def closeEvent(self, event):
        self.stop_camera()  # Stop the camera when the widget is closed
        event.accept()  # Ensure the event is accepted to close the window