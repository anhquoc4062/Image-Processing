import sys
import cv2 as cv
import qdarkgraystyle

from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow, QFileDialog, QAction, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QIcon

from basicdip import BasicImageProcessing as BIP

#filename = ""
class UI(QtWidgets.QMainWindow):

    def __init__(self):
        self.filename = ""
        super(UI, self).__init__()
        uic.loadUi("interface.ui", self)
        self.setWindowTitle("Image Processing")
        self.show()
        self.Init()
        self.bip = ""
        self.toolbar = False
        self.img_exist = False
        self.x_current = 0
        self.y_current = 0
        self.setWindowIcon(QIcon("images/icon/mainicon.png"))
        self.curImg = False
        #self.test()

    def Init(self):
        #bắt các sự kiện action
        self.actionOpenImage.triggered.connect(self.openimage)
        self.actionChuong3.triggered.connect(self.chuong3_clicked)
        self.actionChuong4.triggered.connect(self.chuong4_clicked)
        self.actionChuong5.triggered.connect(self.chuong5_clicked)
        self.actionChuong7.triggered.connect(self.chuong7_clicked)
        self.actionChuong8.triggered.connect(self.chuong8_clicked)
        self.actionSave.triggered.connect(self.saveImg)

        #bắt sự kiện các input
        #chương 2
        self.rotation_inp.valueChanged.connect(self.rotation)
        self.scaling_inp.valueChanged.connect(self.scaling)
        self.tranX_inp.valueChanged.connect(self.getTranX)
        self.tranY_inp.valueChanged.connect(self.getTranY)
        self.affine_inp.valueChanged.connect(self.affine)

        #Chương 3
        self.log_inp.valueChanged.connect(self.log)
        self.gamma_inp.valueChanged.connect(self.gamma)

        #chương 4
        self.median_inp.valueChanged.connect(self.median)
        self.gaussian_inp.valueChanged.connect(self.gaussian)
        self.highboost_inp.valueChanged.connect(self.highBoost)
        self.average_inp.valueChanged.connect(self.avg)

        #chuongw 7
        self.morphology_inp.valueChanged.connect(self.morphology)

        #Checkbox
        self.chuong2Check.stateChanged.connect(self.groupBox2Enable)
        self.chuong3Check.stateChanged.connect(self.groupBox3Enable)
        self.chuong4Check.stateChanged.connect(self.groupBox4Enable)
        self.chuong7Check.stateChanged.connect(self.groupBox7Enable)


    def test(self, m):
        self.median_val.setText(str(m))

    def saveImg(self):
        img = self.curImg
        # size đến tên hình =36
        s = self.filename[0]
        print(s)
        photoName = ""
        for i in range(len(s) - 1, 0, -1):
            if s[i] == '/':
                photoName = s[i + 1:len(s) - 4]
                photoName = photoName + "_Changed" + s[len(s) - 4:]
                break

        q = QMessageBox.question(self, "Xác nhận", "Lưu ảnh hiện tại?", QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)
        if (q == QMessageBox.Yes):
            cv.imwrite(photoName, img)
            QMessageBox.about(self, "Thông báo", "Lưu ảnh thành công.")
            

    def groupBox2Enable(self):
        if (self.img_exist == True):
            if self.chuong2Check.isChecked():
                self.chuong2Group.setEnabled(True)
                self.scaling_inp.setEnabled(True)
                self.scaling_val.setEnabled(True)
            else:
                self.chuong2Group.setEnabled(False)
        else:
            self.chuong2Check.setChecked(False)
            QMessageBox.about(self, "Thông Báo", "Chưa chọn hình ?!!")

    def groupBox3Enable(self):
        if (self.img_exist == True):
            if self.chuong3Check.isChecked():
                self.chuong3Group.setEnabled(True)
            else:
                self.chuong3Group.setEnabled(False)
        else:
            self.chuong3Check.setChecked(False)
            QMessageBox.about(self, "Thông Báo", "Chưa chọn hình ?!!")

    def groupBox4Enable(self):
        if (self.img_exist == True):
            if self.chuong4Check.isChecked():
                self.chuong4Group.setEnabled(True)
            else:
                self.chuong4Group.setEnabled(False)
        else:
            self.chuong4Check.setChecked(False)
            QMessageBox.about(self, "Thông Báo", "Chưa chọn hình ?!!")

    def groupBox7Enable(self):
        if (self.img_exist == True):
            if self.chuong7Check.isChecked():
                self.chuong7Group.setEnabled(True)
            else:
                self.chuong7Group.setEnabled(False)
        else:
            self.chuong7Check.setChecked(False)
            QMessageBox.about(self, "Thông Báo", "Chưa chọn hình ?!!")

    def openimage(self):
        self.filename = QFileDialog.getOpenFileName(self, "Choose Image", "","Images File(*.jpg; *.jpeg; *.png);;Python Files (*.py)")
        #print (self.filename[0])
        if(self.filename[0] != ''):
            width = self.labelOriginal.width()
            height = self.labelOriginal.height()
            self.labelOriginal.setPixmap(QPixmap(self.filename[0]).scaled(width, height))
            self.labelChanged.setPixmap(QPixmap(self.filename[0]).scaled(width, height))
            width = self.labelOriginal.width()
            height = self.labelOriginal.height()
            self.bip = BIP(self.filename[0], width, height)
            self.img_exist = True

    def bindingToLabel(self, changed_img):
        qformat = QImage.Format_Indexed8
        self.curImg=changed_img

        if len(changed_img.shape) == 3:
            if (changed_img.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(changed_img, changed_img.shape[1], changed_img.shape[0], changed_img.strides[0], qformat)
        # BGR > RGB
        img = img.rgbSwapped()
        self.labelChanged.setPixmap(QPixmap.fromImage(img))
        self.labelChanged.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def negative(self):
        res = self.bip.negative()
        self.bindingToLabel(res)

    def histogram(self):
        res = self.bip.histogram()
        self.bindingToLabel(res)

    def orignal(self):
        res = self.bip.original()
        self.bindingToLabel(res)

    def log(self, m):
        self.log_val.setText(str(m))
        res = self.bip.log(m)
        self.bindingToLabel(res)

    def gamma(self, m):
        self.gamma_val.setText(str("{0:.1f}".format(round(m*0.1, 1))))
        res = self.bip.gamma(m*0.1)
        self.bindingToLabel(res)

    def getTranX(self, x):
        self.tranX_val.setText(str(x))
        self.translation()

    def getTranY(self, y):
        self.tranY_val.setText(str(y))
        self.translation()

    def translation(self):
        x = int(self.tranX_val.text())
        y = int(self.tranY_val.text())
        res = self.bip.translation(x, y)
        self.bindingToLabel(res)

    def scaling(self, size):
        res = self.bip.scaling(size)
        self.scaling_val.setText(str(size) + "%")
        self.bindingToLabel(res)

    def rotation(self, angle):
        self.rotation_val.setText(str(angle)+"°")
        res = self.bip.rotation(angle)
        self.bindingToLabel(res)

    def affine(self, m):
        self.affine_val.setText(str(m))
        res = self.bip.affine(m)
        self.bindingToLabel(res)

    #Chuong4

    def avg(self, m):
        self.average_val.setText(str(m * 2 - 1))
        size = int(self.average_val.text())
        res = self.bip.avg(size)
        self.bindingToLabel(res)

    def gaussian(self, m):
        self.gaussian_val.setText(str(m * 2 - 1))
        size = int(self.gaussian_val.text())
        res = self.bip.gaussian(size)
        self.bindingToLabel(res)

    def median(self, m):
        self.median_val.setText(str(m*2-1))
        size = int(self.median_val.text())
        res = self.bip.median(size)
        self.bindingToLabel(res)

    def unMark(self):
        res=self.bip.unMark()
        self.bindingToLabel(res)

    def laplacian(self):
        res=self.bip.laplacian()
        self.bindingToLabel(res)

    def compositeLaplacian(self):
        res=self.bip.compositeLaplacian()
        self.bindingToLabel(res)

    def highBoost(self, m):
        self.highboost_val.setText(str(m))
        A = int(self.highboost_val.text())
        res = self.bip.highBoost(A*1.0)
        self.bindingToLabel(res)

    def fourier(self):
        res=self.bip.fourier()
        #self.bindingToLabel(res)

    def highPass(self):
        res=self.bip.highPassGaussian()
        self.bindingToLabel(res)

    def canny(self):
        res=self.bip.Canny()
        self.bindingToLabel(res)

    #chương 7
    def morphology(self, m):
        self.morphology_val.setText(str(m))
        res = self.bip.morphology(m)
        self.bindingToLabel(res)
    def open(self):
        res = self.bip.open()
        self.bindingToLabel(res)
    def close(self):
        res = self.bip.close()
        self.bindingToLabel(res)
    def gradient(self):
        res = self.bip.gradient()
        self.bindingToLabel(res)
    def morboundary(self):
        res = self.bip.morboundary()
        self.bindingToLabel(res)
    def convex(self):
        res = self.bip.convex()
        self.bindingToLabel(res)

    #chương 8
    def sobelx(self):
        res = self.bip.sobelX()
        self.bindingToLabel(res)
    def sobely(self):
        res = self.bip.sobelY()
        self.bindingToLabel(res)
    def lapcian(self):
        res = self.bip.lapcian()
        self.bindingToLabel(res)

    #triggered event
    def chuong3_clicked(self):
        if (self.img_exist == True):
            self.chuong3Check.setChecked(True)
            if (self.toolbar == False):
                self.toolbar = self.addToolBar('Toolbar')
            else:
                self.toolbar.clear()
            actionOriginal = QAction(QIcon('images/icon/original.png'), 'Original', self)
            actionOriginal.triggered.connect(self.orignal)


            actionNegative = QAction(QIcon('images/icon/negative.png'), 'Negative', self)
            actionNegative.triggered.connect(self.negative)


            actionHistogram = QAction(QIcon('images/icon/histogram.png'), 'Histogram', self)
            actionHistogram.triggered.connect(self.histogram)

            self.toolbar.clear()
            self.toolbar.addAction(actionOriginal)
            self.toolbar.addAction(actionNegative)
            self.toolbar.addAction(actionHistogram)
            self.chuong3Group.setEnabled(True)
        else:
            QMessageBox.about(self, "Thông Báo", "Chưa chọn hình ?!!")

    def chuong4_clicked(self):
        if (self.img_exist == True):
            self.chuong4Check.setChecked(True)
            if (self.toolbar == False):
                self.toolbar = self.addToolBar('Toolbar')
            else:
                self.toolbar.clear()

            actionUnSharp = QAction(QIcon('images/icon/unsharp.png'), 'Unsharp', self)
            actionUnSharp.triggered.connect(self.unMark)

            actionLaplacian = QAction('Laplacian', self)
            actionLaplacian.triggered.connect(self.laplacian)

            actionCLaplacian = QAction('Composite Laplacian', self)
            actionCLaplacian.triggered.connect(self.compositeLaplacian)
            self.toolbar.addAction(actionUnSharp)
            self.toolbar.addAction(actionLaplacian)
            self.toolbar.addAction(actionCLaplacian)

            self.chuong4Group.setEnabled(True)

        else:
            QMessageBox.about(self, "Thông Báo", "Chưa chọn hình ?!!")

    #Chương 5
    def chuong5_clicked(self):
        if (self.img_exist == True):
            if (self.toolbar == False):
                self.toolbar = self.addToolBar('Toolbar')
            else:
                self.toolbar.clear()
            actionFourier = QAction('Fourier', self)
            actionFourier.triggered.connect(self.fourier)

            actionHighPass = QAction('High-Pass Filter', self)
            actionHighPass.triggered.connect(self.highPass)

            self.toolbar.addAction(actionFourier)
            self.toolbar.addAction(actionHighPass)
        else:
            QMessageBox.about(self, "Thông Báo", "Chưa chọn hình ?!!")

    #chương 7
    def chuong7_clicked(self):
        if (self.img_exist == True):
            self.chuong7Check.setChecked(True)
            if (self.toolbar == False):
                self.toolbar = self.addToolBar('Toolbar')
            else:
                self.toolbar.clear()

            actionOpen = QAction(QIcon('images/icon/open.png'), 'Open', self)
            actionOpen.triggered.connect(self.open)
            self.toolbar.addAction(actionOpen)

            actionClose = QAction(QIcon('images/icon/close.png'), 'Close', self)
            actionClose.triggered.connect(self.close)
            self.toolbar.addAction(actionClose)

            actionGradient = QAction(QIcon('images/icon/gradient.png'), 'Gradient', self)
            actionGradient.triggered.connect(self.gradient)
            self.toolbar.addAction(actionGradient)

            actionMorboundary = QAction(QIcon('images/icon/morboundary.png'), 'Morboundary', self)
            actionMorboundary.triggered.connect(self.morboundary)
            self.toolbar.addAction(actionMorboundary)

            actionConvex = QAction(QIcon('images/icon/convex.png'), 'Convex', self)
            actionConvex.triggered.connect(self.convex)
            self.toolbar.addAction(actionConvex)

            self.chuong7Group.setEnabled(True)

        else:
            QMessageBox.about(self, "Thông Báo", "Chưa chọn hình ?!!")

    def chuong8_clicked(self):
        if (self.img_exist == True):
            if (self.toolbar == False):
                self.toolbar = self.addToolBar('Toolbar')
            else:
                self.toolbar.clear()

            actionSobelX = QAction(QIcon('images/icon/sobelx.png'), 'SobelX', self)
            actionSobelX.triggered.connect(self.sobelx)
            self.toolbar.addAction(actionSobelX)

            actionSobelY = QAction(QIcon('images/icon/sobely.png'), 'SobelY', self)
            actionSobelY.triggered.connect(self.sobely)
            self.toolbar.addAction(actionSobelY)

            actionLapcian = QAction(QIcon('images/icon/laplacian.png'), 'Lapcian', self)
            actionLapcian.triggered.connect(self.lapcian)
            self.toolbar.addAction(actionLapcian)

            actionCanny = QAction(QIcon('images/icon/canny.png'), 'Canny', self)
            actionCanny.triggered.connect(self.canny)
            self.toolbar.addAction(actionCanny)
        else:
            QMessageBox.about(self, "Thông Báo", "Chưa chọn hình ?!!")

if __name__ == "__main__":
    a = QtWidgets.QApplication(sys.argv)
    win = UI()
    sys.exit(a.exec_())

