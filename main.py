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
import threading

# import QT libraries
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QImage, QFont
from PyQt5.QtWidgets import (QApplication, QWidget)
from PyQt5.QtGui import QPixmap
# from PyQt5.QtWidgets import QApplication, QLabel
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

        # todo - start the eeg reader
        # self.eeg_bot = Eeg()

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setStyleSheet("background-color:white;")
        # self.showFullScreen()
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.label = QtWidgets.QLabel(self)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_image)

        # timer set to 1 second
        timer.start(1000)

        # start the composition timer here
        self.start_time = time()

        # while the composition duration is less that the duration
        # while time() < start_time + config.duration_of_composition:
            # self.update_gui()
        self.update_image()

    def update_image(self):
        print("-------- updating gui")

        # todo - every 10 seconds read a new signal from eeg
        # and do audio thing
        # if int(time() % 10) == 0:
        #     self.eeg_bot.read_data()

        # load image from config and display on widget
        pixmap = QtGui.QPixmap(config.image_to_display)
        if not pixmap.isNull():
            self.label.setPixmap(pixmap)
            self.label.adjustSize()
            self.resize(pixmap.size())

        if time() > self.start_time + config.duration_of_composition:
            quit()

    # def update_gui(self):
    #     """Threading event that updates the UI"""
    #     # print("-------- updating gui")
    #
    #     # every 10 seconds read a new signal from eeg
    #     # and do audio thing
    #     # if int(time() % 10) == 0:
    #     #     self.eeg_bot.read_data()
    #
    #     # get the most recent visual file choice from config
    #     self.update_visuals()
    #
    #     # start the thread for the UI
    #     self.update()
    #
    #     # start the UI thread
    #     ui_thread_baud_rate = 1 # in seconds
    #     self.gui_thread = threading.Timer(ui_thread_baud_rate, self.update_gui)
    #     self.gui_thread.start()

    # def update_visuals(self):
        # # might not need this geometry
        # screen_resolution = self.geometry()
        # height = screen_resolution.height()
        # width = screen_resolution.width()
        #
        # # put the cello score image on the UI
        # # self.painter.drawImage(0, 0, config._image_to_display)
        #
        # image_to_show = QImage
        # painter = QPainter(config._image_to_display)

        # label = QLabel(self)
        # pixmap = QPixmap(config.image_to_display)
        # label.setPixmap(pixmap)
        # self.setCentralWidget(label)
        # self.resize(pixmap.width(), pixmap.height())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MainWindow()
    # widget.resize(800, 600)
    # # widget.showFullScreen()
    # widget.setWindowTitle("Digital Syzygies")
    # widget.setStyleSheet("background-color:white;")

    if PLATFORM == "x86_64":
        widget.setCursor(Qt.BlankCursor)

    widget.show()

    sys.exit(app.exec_())
