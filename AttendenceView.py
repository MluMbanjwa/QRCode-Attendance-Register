import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListView, QAbstractItemView
from PyQt6 import QtCore
from PyQt6.QtCore import QStringListModel

class AttendanceView(QWidget):
    def __init__(self, file_name=''):
        super().__init__()

        self.label = QLabel(self)
        self.attendees = []  # List to store attendee names
        self.model = QStringListModel(self.attendees)
        self.view = QListView(self)
        self.view.setModel(self.model)

        self.view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)

        self.setWindowTitle("Attendance View")
        self.setFixedSize(500, 500)
        self.personel = set()
        self.row = 1  # Start writing from row 1 in Excel

        self.show()

    def addAttendee(self, name: str = ""):
        if name in self.personel:
            return
        self.personel.add(name)

        time = QtCore.QTime.currentTime().toString()
        attendee_text = f"{self.attendees.__len__()+1}.{name} Arrived at {str(time)}"
        self.updateLabel(attendee_text)
        self.attendees.append(attendee_text)
        self.model.setStringList(self.attendees)
        self.view.scrollTo(self.model.index(len(self.attendees) - 1))

    def updateLabel(self, details):
        list_details = details.split("\n")
        if len(list_details) > 1:
            self.label.setText(details)
        QTimer.singleShot(2000, lambda: self.label.setText("decrease the brightness")).singleShot(2000, lambda: self.label.setText("decrease the brightness"))
            

