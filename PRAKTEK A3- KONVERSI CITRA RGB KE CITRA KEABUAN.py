# Import Library
import sys
import cv2
import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from PyQt5.uic import loadUi

# Membuat class ShowImage
class ShowImage(QMainWindow):
    def __init__(self):
        super(ShowImage, self).__init__()
        loadUi('ShowImageA3.ui', self)
        
        self.image = None  # Variabel untuk menyimpan gambar
        
        # Menghubungkan tombol dengan fungsi
        self.loadButton.clicked.connect(self.loadClicked)
        self.GrayButton.clicked.connect(self.grayClicked)

    @pyqtSlot()
    def loadClicked(self):
        """Memuat gambar saat tombol ditekan"""
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        if filename:
            self.loadImage(filename)

    def loadImage(self, filename):
        """Membaca gambar dari file"""
        self.image = cv2.imread(filename)
        self.displayImage(1)

    def grayClicked(self):
        """Mengonversi gambar menjadi grayscale dan menampilkan matriks piksel"""
        if self.image is None:
            return

        # Mengonversi ke grayscale menggunakan OpenCV
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Simpan gambar grayscale ke variabel utama
        self.image = gray
        
        # Cetak matriks piksel grayscale
        print("Matriks Piksel Citra Keabuan:")
        print(self.image)
        
        # Tampilkan hasil konversi
        self.displayImage(2)

    def displayImage(self, window=1):
        """Menampilkan gambar ke dalam GUI"""
        if self.image is None:
            return

        # Menentukan format gambar
        if len(self.image.shape) == 2:  # Grayscale image
            qformat = QImage.Format_Grayscale8
            img = QImage(self.image.data, self.image.shape[1], self.image.shape[0], self.image.strides[0], qformat)
        else:  # RGB image
            qformat = QImage.Format_RGB888
            img = QImage(self.image.data, self.image.shape[1], self.image.shape[0], self.image.strides[0], qformat)
            img = img.rgbSwapped()  # Mengubah BGR ke RGB

        # Menampilkan gambar sesuai jendela yang dipilih
        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(img))
            self.imgLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.imgLabel.setScaledContents(True)
        elif window == 2:
            self.hasilLabel.setPixmap(QPixmap.fromImage(img))
            self.hasilLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.hasilLabel.setScaledContents(True)

# Membuat window untuk menampilkan GUI
app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('Show Image GUI')
window.show()
sys.exit(app.exec_())
