import sys
import cv2 as cv
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow, QFileDialog, QAction
from PyQt5.QtGui import QPixmap, QImage
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
        #self.test()

    def Init(self):
        #bắt các sự kiện action
        self.actionOpenImage.triggered.connect(self.openimage)
        self.actionChuong2.triggered.connect(self.chuong2_clicked)
        self.actionChuong3.triggered.connect(self.chuong3_clicked)

    def openimage(self):
        self.filename = QFileDialog.getOpenFileName(self, "Choose Image", "","Images File(*.jpg; *.jpeg; *.png);;Python Files (*.py)")
        width = self.labelOriginal.width()
        height = self.labelOriginal.height()
        self.labelOriginal.setPixmap(QPixmap(self.filename[0]).scaled(width, height))
        width = self.labelOriginal.width()
        height = self.labelOriginal.height()
        self.bip = BIP(self.filename[0], width, height)

    def bindingToLabel(self, changed_img):
        q_changed_img = QImage(changed_img, changed_img.shape[1], changed_img.shape[0], changed_img.shape[1] * 3,
                               QImage.Format_RGB888)
        pix = QPixmap(q_changed_img)
        self.labelChanged.setPixmap(QPixmap(pix))

    def negative(self):
        res = self.bip.negative()
        self.bindingToLabel(res)

    def histogram(self):
        res = self.bip.histogram()
        self.bindingToLabel(res)

    def orignal(self):
        res = self.bip.original()
        self.bindingToLabel(res)

    def log(self):
        res = self.bip.log()
        self.bindingToLabel(res)

    def translation(self):
        res = self.bip.translation()
        self.bindingToLabel(res)

    def scaling(self):
        res = self.bip.scaling()
        self.bindingToLabel(res)

    def rotation(self):
        res = self.bip.rotation()
        self.bindingToLabel(res)

    def affine(self):
        res = self.bip.affine()
        self.bindingToLabel(res)

    def chuong2_clicked(self):

        actionTranslation = QAction('Translation', self)
        actionTranslation.triggered.connect(self.translation)

        actionScaling = QAction('Scaling', self)
        actionScaling.triggered.connect(self.scaling)

        actionRotation = QAction('Rotation', self)
        actionRotation.triggered.connect(self.rotation)

        actionAffine = QAction('Affine', self)
        actionAffine.triggered.connect(self.affine)

        self.toolbar = self.addToolBar('Chương 2')
        self.toolbar.addAction(actionTranslation)
        self.toolbar.addAction(actionScaling)
        self.toolbar.addAction(actionRotation)
        self.toolbar.addAction(actionAffine)

    def chuong3_clicked(self):

        actionOriginal = QAction('Original', self)
        actionOriginal.triggered.connect(self.orignal)


        actionNegative = QAction('Negative', self)
        actionNegative.triggered.connect(self.negative)


        actionHistogram = QAction('Histogram', self)
        actionHistogram.triggered.connect(self.histogram)


        actionLog = QAction('Log', self)
        actionLog.triggered.connect(self.log)

        actionExponential = QAction('Exponential', self)
        actionExponential.triggered.connect(self.orignal)

        self.toolbar = self.addToolBar('Chương 3')
        self.toolbar.addAction(actionOriginal)
        self.toolbar.addAction(actionNegative)
        self.toolbar.addAction(actionHistogram)
        self.toolbar.addAction(actionLog)
        self.toolbar.addAction(actionExponential)

    #def test(self):


if __name__ == "__main__":
    a = QtWidgets.QApplication(sys.argv)
    win = UI()
    sys.exit(a.exec_())

