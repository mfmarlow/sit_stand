import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QObject
from PySide2.QtWidgets import QLCDNumber, QStackedWidget, QWidget

class MainPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()

        sitLabel = QtWidgets.QLabel("Sit Time")
        standLabel = QtWidgets.QLabel("Stand Time")

        sitField = QtWidgets.QTimeEdit()
        sitField.setDisplayFormat('hh:mm:ss')
        
        standField = QtWidgets.QTimeEdit()
        standField.setDisplayFormat('hh:mm:ss')
        
        sitButton = QtWidgets.QPushButton("Start Sitting")
        sitButton.clicked.connect(lambda:self.newTimer(SIT_TIMER, sitField.time()))
        standButton = QtWidgets.QPushButton("Start Standing")
        standButton.clicked.connect(lambda:self.newTimer(STAND_TIMER, standField.time()))

        gridLayout = QtWidgets.QGridLayout()
        gridLayout.addWidget(sitLabel, 0, 0)
        gridLayout.addWidget(standLabel, 0, 1)
        gridLayout.addWidget(sitField, 1, 0)
        gridLayout.addWidget(standField, 1, 1)
        gridLayout.addWidget(sitButton, 2, 0)
        gridLayout.addWidget(standButton, 2, 1)

        self.setLayout(gridLayout)
    
    def newTimer(self, sitStandID, inputTime):
        timerWidget = TimerPage(sitStandID, inputTime)
        main.addWidget(timerWidget)
        main.setCurrentIndex(TIMER_PAGE)


class Timer(QLCDNumber):
    def __init__(self, inputTime):
        super().__init__()

        self.countdownTimer = QtCore.QTimer(self)
        self.countdownTimer.setTimerType(QtCore.Qt.VeryCoarseTimer)
        self.countdownTimer.setSingleShot(True)
        self.countdownTimer.start(QtCore.QTime(0,0).msecsTo(inputTime))

        updateTimer = QtCore.QTimer(self)
        updateTimer.timeout.connect(self.showTimeLeft)
        updateTimer.start(1000)

        self.setDigitCount(8)
        self.showTimeLeft()

    def showTimeLeft(self):
        #get time remaining in hh:mm:ss format
        msLeft = self.countdownTimer.remainingTime()
        timeLeft = QtCore.QTime(0,0).addMSecs(msLeft)
        text = timeLeft.toString('hh:mm:ss')
        self.display(text)

class TimerPage(QtWidgets.QWidget):
    def __init__(self, sitStandID, inputTime):
        super().__init__()
        
        menuButton = QtWidgets.QPushButton("Menu")
        menuButton.clicked.connect(lambda:main.removeWidget(main.currentWidget()))

        statusLabel = QtWidgets.QLabel()
        statusLabel.setText("Currently: Sitting") if (sitStandID == SIT_TIMER) else statusLabel.setText("Currently: Standing")

        timerBox = Timer(inputTime)

        skipButton = QtWidgets.QPushButton("Done")

        gridLayout = QtWidgets.QGridLayout()
        gridLayout.addWidget(menuButton, 0, 0)
        gridLayout.addWidget(statusLabel, 1, 0)
        gridLayout.addWidget(timerBox, 2, 0)
        gridLayout.addWidget(skipButton, 3, 0)

        self.setLayout(gridLayout)

# Constants
MAIN_PAGE = 0
TIMER_PAGE = 1
SIT_TIMER = 0
STAND_TIMER = 1

# Create Qt App
app = QtWidgets.QApplication(sys.argv)
app.setApplicationDisplayName("Sit_Stand")

# Create and Show Elements
main = QStackedWidget()
homeWidget = MainPage()

main.addWidget(homeWidget)
main.setGeometry(100, 100, 500, 355)
main.show()

# Run Qt main loop
app.exec_()
