# Import Library
import sys
import cv2
import numpy as np
import math
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from PyQt5.uic import loadUi

# Membuat class ShowImage
class ShowImage(QMainWindow):
    def __init__(self):
        super(ShowImage, self).__init__()
        loadUi('ShowImageA7.ui', self)
        
        self.image = None  # Variabel untuk menyimpan gambar asli
        self.processed_image = None  # Variabel untuk menyimpan gambar hasil pemrosesan
        self.brightness = 1  # Default brightness
        self.contrast = 1  # Default contrast
        
        # Menghubungkan tombol dengan fungsi
        self.loadButton.clicked.connect(self.loadClicked)
        self.GrayButton.clicked.connect(self.grayClicked)
        self.PereganganObjek.clicked.connect(self.pereganganKontras)
        self.Negativ.clicked.connect(self.negatifCitra)
        
        # Menggunakan slider dari UI untuk mengatur brightness
        self.brightnessSlider = self.SliderBrightness
        self.brightnessSlider.setMinimum(0)
        self.brightnessSlider.setMaximum(100)
        self.brightnessSlider.setValue(self.brightness)
        self.brightnessSlider.valueChanged.connect(self.updateBrightness)

        # Menggunakan slider dari UI untuk mengatur contrast
        self.contrastSlider = self.SliderKontras
        self.contrastSlider.setMinimum(10)  # Skala 1.0 = 10
        self.contrastSlider.setMaximum(50)  # Skala 5.0 = 50
        self.contrastSlider.setValue(int(self.contrast * 10))
        self.contrastSlider.valueChanged.connect(self.updateContrast)

    @pyqtSlot()
    def loadClicked(self):
        """Memuat gambar saat tombol ditekan"""
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        if filename:
            self.loadImage(filename)

    def loadImage(self, filename):
        """Membaca gambar dari file"""
        self.image = cv2.imread(filename)
        self.processed_image = self.image.copy()
        self.displayImage(1)

    def updateBrightness(self, value):
        """Memperbarui nilai brightness dari slider"""
        self.brightness = value
        self.grayClicked()

    def updateContrast(self, value):
        """Memperbarui nilai contrast dari slider"""
        self.contrast = value / 10.0  # Konversi dari slider ke skala asli
        self.grayClicked()

    def grayClicked(self):
        """Mengonversi gambar menjadi grayscale dan menampilkan matriks piksel"""
        if self.image is None:
            return

        # Konversi citra RGB ke grayscale menggunakan OpenCV
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # Tambahkan brightness dengan proses clipping
        img = np.clip(img + self.brightness, 0, 255).astype(np.uint8)
        
        # Terapkan contrast dengan proses clipping
        img = np.clip(img * self.contrast, 0, 255).astype(np.uint8)
        
        # Simpan gambar hasil pemrosesan
        self.processed_image = img
        
        # Cetak matriks piksel grayscale dengan brightness dan contrast
        print("Matriks Piksel Citra Keabuan dengan Brightness dan Kontras:")
        print(self.processed_image)
        
        # Tampilkan hasil konversi
        self.displayImage(2)
    
    def pereganganKontras(self):
        """Melakukan peregangan kontras pada citra grayscale"""
        if self.processed_image is None:
            return
        
        # Tentukan nilai maksimum dan minimum piksel
        min_pixel = 0
        max_pixel = 255
        
        # Menerapkan rumus peregangan kontras
        img = self.processed_image.astype(np.float32)
        img = (img - np.min(img)) / (np.max(img) - np.min(img)) * (max_pixel - min_pixel) + min_pixel
        img = np.clip(img, min_pixel, max_pixel).astype(np.uint8)
        
        # Simpan hasilnya dan tampilkan
        self.processed_image = img
        print("Matriks Piksel Citra Setelah Peregangan Kontras:")
        print(self.processed_image)
        self.displayImage(2)

    def negatifCitra(self):
        """Melakukan transformasi negatif pada citra grayscale"""
        if self.processed_image is None:
            return
        
        # Tentukan nilai maksimum intensitas
        max_intensity = 255
        
        # Terapkan transformasi negatif citra
        img = max_intensity - self.processed_image
        
        # Simpan hasilnya dan tampilkan
        self.processed_image = img
        print("Matriks Piksel Citra Setelah Transformasi Negatif:")
        print(self.processed_image)
        self.displayImage(2)

    def displayImage(self, window=1):
        """Menampilkan gambar ke dalam GUI"""
        if self.processed_image is None:
            return

        # Menentukan format gambar
        if len(self.processed_image.shape) == 2:  # Grayscale image
            qformat = QImage.Format_Grayscale8
            img = QImage(self.processed_image.data, self.processed_image.shape[1], self.processed_image.shape[0], self.processed_image.strides[0], qformat)
        else:  # RGB image
            qformat = QImage.Format_RGB888
            img = QImage(self.processed_image.data, self.processed_image.shape[1], self.processed_image.shape[0], self.processed_image.strides[0], qformat)
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
