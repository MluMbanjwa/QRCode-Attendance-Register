import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QSplashScreen,QDialog
)
import sqlite3
import QRCodeGenerato as Qr
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap,QColor
from cameraViewWidget import CameraView
from AttendenceView import AttendanceView
from MeetingDetailsWindow import meetingDetailsInput
from MeetingsBrowser import TableViewer

class LoadingDialog(QDialog):
    def __init__(self, message="Loading..."):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setModal(True)
        self.setFixedSize(200, 100)

        self.setProperty("class", "bubble")  # <- This is your CSS hook

        layout = QVBoxLayout()
        label = QLabel(message)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)

class Win(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(400)
        self.setFixedHeight(500)
        self.lay = QVBoxLayout(self)
        self.connection = sqlite3.connect("dataBase.db")
        self.cursur = self.connection.cursor()
        self.start = QPushButton("Start Meeting", self)
        self.stop = QPushButton("Close", self)
        self.view = QPushButton('View Past Meetings', self)
        self.addQrcode = Qr.QRCodeGenerator()

        self.btnLay = QHBoxLayout()
        self.btnLay.addWidget(self.stop)
        self.btnLay.addWidget(self.start)

        self.winInput = meetingDetailsInput()
        
        self.lay.addWidget(self.view)
        self.lay.addWidget(self.winInput)
        self.lay.addLayout(self.btnLay)
        self.lay.addWidget(QLabel())
        self.lay.addWidget(self.addQrcode)
        

        self.start.clicked.connect(self.finishInput)
        self.stop.clicked.connect(self.shutdown)
        self.view.clicked.connect(self.viewPastMeetings)

        self.setWindowTitle("Attendance Register App")


        self.show()

    def entry(self, name: str):
        if name == self.winCamera.version:
            self.shutdown()
        else:
            self.winAttend.addAttendee(name)
            self.writeToDataBase(name)

    def writeToDataBase(self, name: str):
        self.cursur.execute(
            "INSERT OR IGNORE INTO Data(Meeting_Date, Meeting_Time, Meeting_Name, Teacher_Name, Teacher_Arrival_Time) VALUES (?, ?, ?, ?, ?)",
            (
                self.winInput.getDate(),
                self.winInput.getTime(),
                self.winInput.getName(),
                name,
                QtCore.QTime.currentTime().toString("HH:mm")
            )
        )
        self.connection.commit()

    def finishInput(self):
        load=LoadingDialog("Setting up meeting")
        
        load.show()
        name = self.winInput.name.text()
        date = self.winInput.date.text()
        time = self.winInput.time.text()
        details = f"Meeting: {name}\nDate: {date}\nTime: {time}"
        self.winCamera = CameraView()
        self.winAttend = AttendanceView()
        self.winCamera.setMinimumWidth(900)
        self.winLay = QHBoxLayout()
        self.winLay.addWidget(self.winAttend)
        self.winLay.addWidget(self.winCamera)
        self.lay.addLayout(self.winLay)
        self.winAttend.updateLabel(details)
        self.stop.setEnabled(True)
        self.start.setEnabled(False)
        self.winInput.setEnabled(False)
        self.winInput.hide()
        self.winCamera.read.connect(self.entry)
        self.showFullScreen()
        #self.stop.setEnabled(False)  # Confirm if principal approves
        self.addQrcode.setEnabled(False)
        self.view.setEnabled(False)
        load.close

    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def shutdown(self):
        if hasattr(self, 'winCamera'):
            self.winCamera.stop_camera()
        if hasattr(self, 'winAttend'):
            self.winAttend.close()
        self.connection.close()
        self.close()

    def viewPastMeetings(self):
        details = f"Browser Past meetings and export the desired Attendance Register(s)"
        self.winLay = QHBoxLayout()
        view = TableViewer()
        self.winLay.addWidget(view)
        self.lay.addLayout(self.winLay)
        if hasattr(self, 'winAttend'):
            self.winAttend.updateLabel(details)
        self.showFullScreen()
        self.stop.setEnabled(True)
        self.stop.setText("Close")
        self.start.setEnabled(False)
        self.winInput.setEnabled(False)
        self.winInput.hide()
        self.view.setEnabled(False)
        
        
# Main app

app = QApplication(sys.argv)
window = Win()

with open('assets/background.css', 'r') as file:
    window.setStyleSheet(file.read())   
sys.exit(app.exec())
