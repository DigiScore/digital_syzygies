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
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtGui import QPainter, QPen, QColor, QImage, QFont
from PyQt5.QtWidgets import (QApplication, QWidget)

# import project libraries
import config
from eeg import Eeg

# which platform is this machine?
PLATFORM = platform.machine()

class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # start the eeg reader
        self.eeg_bot = Eeg()

        # start the composition timer here
        start_time = time()

        # start QT painting
        self.painter = QPainter(self)
        self.painter.setRenderHint(QPainter.Antialiasing, True)

        # while the composition duration is less that the duration
        while time() < start_time + config.duration_of_composition:
            self.update_gui()

    def update_gui(self):
        """Threading event that updates the UI"""
        # print("-------- updating gui")

        # every 10 seconds read a new signal from eeg
        # and do audio thing
        if int(time() % 10) == 0:
            self.eeg_bot.read_data()

        # get the most recent visual file choice from config
        self.update_visuals()

        # start the thread for the UI
        self.update()

        # start the UI thread
        ui_thread_baud_rate = 1 # in seconds
        self.gui_thread = threading.Timer(ui_thread_baud_rate, self.update_gui)
        self.gui_thread.start()

    def update_visuals(self):
        # might not need this geometry
        screen_resolution = self.geometry()
        height = screen_resolution.height()
        width = screen_resolution.width()

        # put the cello score image on the UI
        self.painter.drawImage(0, 0, config.image_to_display)


if __name__ =='__main__':
    if __name__ == "__main__":
        app = QApplication(sys.argv)

        widget = MyWidget()
        widget.resize(800, 600)
        # widget.showFullScreen()
        widget.setWindowTitle("Digital Syzygies")
        widget.setStyleSheet("background-color:white;")

        if PLATFORM == "x86_64":
            widget.setCursor(Qt.BlankCursor)

        widget.show()

        sys.exit(app.exec_())
