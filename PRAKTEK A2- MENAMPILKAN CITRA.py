import sys
import cv2
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi

class ShowImage(QMainWindow):
    def __init__(self):
        super(ShowImage, self).__init__()
        loadUi('ShowImageA2.ui', self)
        self.image = None
        self.loadButton.clicked.connect(self.loadClicked)

    @pyqtSlot()
    def loadClicked(self):
        self.loadImage('nadi_doktersehat.jpg')

    def loadImage(self, flname):
        self.image = cv2.imread(flname)
        if self.image is not None:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)  # Konversi ke grayscale
        self.displayImage()

    def displayImage(self):
        if self.image is None:
            return

        qformat = QImage.Format_Grayscale8  # Format untuk gambar grayscale
        img = QImage(self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0], qformat)
        img = img.rgbSwapped()

        pixmap = QPixmap.fromImage(img)
        self.imgLabel.setPixmap(pixmap)
        self.imgLabel.setScaledContents(True)  # Menyesuaikan gambar agar pas dengan label
        self.imgLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

app = QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('Show Image GUI')
window.show()
sys.exit(app.exec_())
