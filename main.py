######################################
#
# Digital Syzygies
#
# code by Craig Vear & William Vear
#
# August 2022
#
# for a composition by Andrew Hugill
#
######################################

# import python libraries
from time import time
import sys
import platform

# import QT libraries
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui, QtWidgets

# import project libraries
import config
from eeg import Eeg
import visuals

# which platform is this machine?
PLATFORM = platform.machine()

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 600
        self.title = "Digital Syzygies"

        # start visual thread
        visuals.main()

        # start the eeg reader andf audio bot
        self.eeg_bot = Eeg()

        # build the UI widget for visual score
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setStyleSheet("background-color:white;")
        if config.full_screen:
            self.showFullScreen()
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.label = QtWidgets.QLabel(self)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_image)

        # timer set to 1 second
        timer.start(1000)

        # start the composition timer here
        self.start_time = time()

        # while the composition duration is less that the duration
        self.update_image()

    def update_image(self):
        # print("-------- updating gui")

        # load image from config and display on widget
        pixmap = QtGui.QPixmap(config.image_to_display)
        if not pixmap.isNull():
            self.label.setPixmap(pixmap)
            self.label.adjustSize()
            self.resize(pixmap.size())

        if time() > self.start_time + config.duration_of_composition:
            self.terminate()

    def terminate(self):
        # terminate all streams - audio may play out.
        self.eeg_bot.terminate()
        visuals.terminate()
        quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MainWindow()

    if PLATFORM == "x86_64":
        widget.setCursor(Qt.BlankCursor)

    widget.show()

    sys.exit(app.exec_())
