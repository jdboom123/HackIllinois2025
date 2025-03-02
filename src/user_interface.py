import PySide6
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QStackedWidget, QLabel
import subprocess


class StartScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()

        self.text = QtWidgets.QLabel("John Deere Autonomous Vehicle",alignment=QtCore.Qt.AlignCenter)
        self.button1 = QtWidgets.QPushButton("Navigate Course")
        self.button2 = QtWidgets.QPushButton("3D Scan")
        self.closebutton = QtWidgets.QPushButton("Close App")

        # Style the Text
        self.text.setStyleSheet("""
            QLabel{  
                color: white;
                font-size: 50px;
                font-weight: bold;
                padding: 10px;
                border-radius: 10px;
            }
        """)
        # Style the buttons
        self.button1.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 30px;
                font-weight: bold;
                padding: 10px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        self.button2.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                font-size: 30px;
                font-weight: bold;
                padding: 10px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)

        self.closebutton.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-size: 30px;
                font-weight: bold;
                padding: 10px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        # self.layout.addWidget(self.closebutton)
    
        self.button1.clicked.connect(self.button1press)
        self.button2.clicked.connect(self.button2press)
        self.closebutton.clicked.connect(self.closebuttonpress)

    def button1press(self):
        # Start a program dedicated to this button.
        self.stacked_widget.setCurrentIndex(1)
    
    def button2press(self):
        # Start a program dedicated to this button.
        self.stacked_widget.setCurrentIndex(2)
    
    def closebuttonpress(self):
        self.close()

class Button1Screen(QtWidgets.QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.process = None

        self.text = QtWidgets.QLabel("Currently Navigating",alignment=QtCore.Qt.AlignCenter)
        self.button3 = QtWidgets.QPushButton("Go Back")

        self.text.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: blue;
                background-color: lightgray;
                padding: 10px;
                border: 2px solid black;
                border-radius: 10px;
            }
        """)

        self.button3.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-size: 30px;
                font-weight: bold;
                padding: 10px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button3)
    
        self.button3.clicked.connect(self.button3press)
        
    def button1press(self):
        if self.process is None:
                self.process = subprocess.Popen["python", "search.py"]
        self.stacked_widget.setCurrentIndex(1)

    def button3press(self):
        # Stop current program and return to home screen.
        if self.process:
                self.process.terminate()
                self.process.wait()
                self.process = None
        
        self.stacked_widget.setCurrentIndex(0)

class Button2Screen(QtWidgets.QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.process = None
        
        self.text = QtWidgets.QLabel("Scanning in progress",alignment=QtCore.Qt.AlignCenter)
        self.button3 = QtWidgets.QPushButton("Go Back")


        self.text.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: blue;
                background-color: lightgray;
                padding: 10px;
                border: 2px solid black;
                border-radius: 10px;
            }
        """)

        self.button3.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-size: 30px;
                font-weight: bold;
                padding: 10px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)

        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button3)
    
        self.button3.clicked.connect(self.button3press)

    def button2press(self):
        print("Button Pressed")
        if self.process is None:
                self.process = subprocess.Popen["python", "3d_scan.py"]
        self.stacked_widget.setCurrentIndex(1)
        
    def button3press(self):
        # Stop current program and return to home screen
        print('goodbye')
        if self.process:
                self.process.terminate()
                self.process.wait()
                self.process = None

        self.stacked_widget.setCurrentIndex(0)

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HackIllinois 2025")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        # Create QStackedWidget to hold the pages
        self.stacked_widget = QStackedWidget()

        # Create pages, passing stacked_widget to each page
        self.page1 = StartScreen(self.stacked_widget)
        self.page2 = Button1Screen(self.stacked_widget)
        self.page3 = Button2Screen(self.stacked_widget)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.page3)

        # Add stacked widget to main layout
        self.layout.addWidget(self.stacked_widget)

        self.setLayout(self.layout)

app = QApplication([])
window = MyWidget()
window.show()
app.exec()

if __name__ == "__main__":
    app = QApplication([])
    window = MyWidget()
    window.resize(1000, 600)
    window.show()
    app.exec()
