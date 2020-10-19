import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QObject
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QLCDNumber, QStackedWidget, QWidget
from win10toast import ToastNotifier
import ctypes
from ctypes import wintypes
lpBuffer = wintypes.LPWSTR()
AppUserModelID = ctypes.windll.shell32.GetCurrentProcessExplicitAppUserModelID
AppUserModelID(ctypes.cast(ctypes.byref(lpBuffer), wintypes.LPWSTR))
appid = lpBuffer.value
ctypes.windll.kernel32.LocalFree(lpBuffer)
if appid is not None:
    print(appid)

class MainPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()

        sitLabel = QtWidgets.QLabel("Sit Time")
        standLabel = QtWidgets.QLabel("Stand Time")

        self.sitField = QtWidgets.QTimeEdit()
        self.sitField.setDisplayFormat('hh:mm:ss')
        
        self.standField = QtWidgets.QTimeEdit()
        self.standField.setDisplayFormat('hh:mm:ss')
        
        sitButton = QtWidgets.QPushButton("Start Sitting")
        sitButton.clicked.connect(lambda:newTimer(self, SIT_TIMER))
        standButton = QtWidgets.QPushButton("Start Standing")
        standButton.clicked.connect(lambda:newTimer(self, STAND_TIMER))

        gridLayout = QtWidgets.QGridLayout()
        gridLayout.addWidget(sitLabel, 0, 0)
        gridLayout.addWidget(standLabel, 0, 1)
        gridLayout.setRowStretch(1,5)
        gridLayout.addWidget(self.sitField, 1, 0)
        gridLayout.addWidget(self.standField, 1, 1)
        gridLayout.addWidget(sitButton, 2, 0)
        gridLayout.addWidget(standButton, 2, 1)

        self.setLayout(gridLayout)

class Timer(QLCDNumber):
    def __init__(self, inputTime):
        super().__init__()

        self.countdownTimer = QtCore.QTimer(self)
        self.countdownTimer.setTimerType(QtCore.Qt.VeryCoarseTimer)
        self.countdownTimer.setSingleShot(True)
        self.countdownTimer.timeout.connect(self.alertUser)
        self.countdownTimer.start(QtCore.QTime(0,0).msecsTo(inputTime))

        updateTimer = QtCore.QTimer(self)
        updateTimer.timeout.connect(self.showTimeLeft)
        updateTimer.start(1000)

        self.setDigitCount(8)
        self.showTimeLeft()

    def showTimeLeft(self):
        #get time remaining in hh:mm:ss format
        msLeft = self.countdownTimer.remainingTime()
        if msLeft > 0 :
            timeLeft = QtCore.QTime(0,0).addMSecs(msLeft)
            text = timeLeft.toString('hh:mm:ss')
            self.display(text)
        else :
            self.display('00:00:00')
    
    def alertUser(self):
        toast = ToastNotifier()
        toast.show_toast("ALERT", "Time is up!", duration=5, threaded= True)

class TimerPage(QtWidgets.QWidget):
    def __init__(self, sitStandID, inputTime):
        super().__init__()
        
        menuButton = QtWidgets.QPushButton("Menu")
        def switchToMainPage():
            oldWidget = main.currentWidget()
            main.removeWidget(oldWidget)
            oldWidget.destroy()
            main.setFixedSize(370, 100)
        menuButton.clicked.connect(switchToMainPage)

        statusLabel = QtWidgets.QLabel()
        statusLabel.setText("Currently: Sitting") if (sitStandID == SIT_TIMER) else statusLabel.setText("Currently: Standing")

        timerBox = Timer(inputTime)

        skipText = "Sit Down Now" if (sitStandID == STAND_TIMER) else "Stand Up Now"
        skipButton = QtWidgets.QPushButton(skipText)
        skipButton.clicked.connect(lambda:newTimer(homeWidget, not sitStandID))

        gridLayout = QtWidgets.QGridLayout()
        gridLayout.addWidget(menuButton, 0, 0)
        gridLayout.addWidget(statusLabel, 1, 0)
        gridLayout.addWidget(timerBox, 2, 0)
        gridLayout.setRowStretch(2,2)
        gridLayout.addWidget(skipButton, 3, 0)

        self.setLayout(gridLayout)


def newTimer(parent, sitStandID):
    inputTime = 0
    inputTime = parent.sitField.time() if (sitStandID == SIT_TIMER) else parent.standField.time()
    timerWidget = TimerPage(sitStandID, inputTime)
    if(main.currentIndex() == TIMER_PAGE):
        oldWidget = main.widget(TIMER_PAGE)
        main.removeWidget(oldWidget)
        oldWidget.destroy()
    main.addWidget(timerWidget)
    main.setCurrentIndex(TIMER_PAGE)
    main.setFixedSize(370, 200)

# Constants
MAIN_PAGE = 0
TIMER_PAGE = 1
SIT_TIMER = 0
STAND_TIMER = 1

# Create Qt App
app = QtWidgets.QApplication(sys.argv)
app.setApplicationDisplayName("Sit_Stand")
icon = QIcon('images/icon.png')
app.setWindowIcon(icon)

# Create and Show Elements
main = QStackedWidget()
homeWidget = MainPage()

main.addWidget(homeWidget)
main.setGeometry(100, 100, 370, 100)
main.setFixedSize(370,100)
main.show()

# Run Qt main loop
app.exec_()
