from PyQt6.QtWidgets import QWidget, QFormLayout, QDateEdit, QTimeEdit, QLineEdit
from PyQt6 import QtCore

class meetingDetailsInput(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QFormLayout(self)
        self.date = QDateEdit(self)
        self.time = QTimeEdit(self)
        self.name = QLineEdit(self)
        self.name.setText("Briefing")
        
        # Set default date and time values
        self.date.setDate(QtCore.QDate.currentDate())
        self.time.setTime(QtCore.QTime.currentTime())
        
        # Add widgets to layout
        self.layout.addRow("Enter Name:", self.name)
        self.layout.addRow("Date:", self.date)
        self.layout.addRow("Start Time:", self.time)
        
        self.setLayout(self.layout)
        self.show()

    # Returns the name as a string
    def getName(self):
        return self.name.text()

    # Returns the date as a string (formatted)
    def getDate(self):
        return self.date.date().toString("yyyy-MM-dd")  # You can adjust the format

    # Returns the time as a string (formatted)
    def getTime(self):
        return self.time.time().toString("HH:mm")  # You can adjust the format


        
 