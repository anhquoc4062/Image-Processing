import sys
import cv2 as cv
import numpy as np
import scipy as sp
from scipy import ndimage
class BasicImageProcessing():
    def __init__(self, _filename, _width, _height):
        self.filename = _filename
        self.width = _width
        self.height = _height
        self.img = cv.imread(self.filename)
        self.img = cv.resize(self.img, (_width, _height))
        self.img_original = self.img
        self.img = cv.cvtColor(self.img, cv.COLOR_BGR2RGB)

    #chuong 3
    def original(self):
        return self.img

    def negative(self):
        res = ~self.img
        return res

    def histogram(self):
        img_yuv = cv.cvtColor(self.img_original, cv.COLOR_BGR2YUV)
        img_yuv[:, :, 0] = cv.equalizeHist(img_yuv[:, :, 0])
        res = cv.cvtColor(img_yuv, cv.COLOR_YUV2RGB)
        return res

    def log(self):
        res_1 = np.uint8(np.log1p(self.img))
        normalized_image = cv.normalize(res_1, None, 0, 255, cv.NORM_MINMAX, dtype=cv.CV_8U)
        thresh = 1
        res_2 = cv.threshold(normalized_image, thresh, 255, cv.THRESH_BINARY)[1]
        return res_2

    #chuong 2
    def scaling(self):
        res = cv.resize(self.img, None, fx = 1.5, fy = 1.5, interpolation = cv.INTER_CUBIC)
        return res

    def translation(self):
        rows, cols, steps = self.img.shape
        M = np.float32([[1, 0, 100], [0, 1, 50]])
        res = cv.warpAffine(self.img, M, (cols, rows))
        return res

    def rotation(self):
        rows, cols,  steps = self.img.shape
        M = cv.getRotationMatrix2D((cols / 2, rows / 2), 90, 1)
        res = cv.warpAffine(self.img, M, (cols, rows))
        return res

    def affine(self):
        rows, cols, ch = self.img.shape

        pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
        pts2 = np.float32([[10, 100], [200, 50], [100, 250]])

        M = cv.getAffineTransform(pts1, pts2)

        res = cv.warpAffine(self.img, M, (cols, rows))
        return res

    #Chương 3

    def avg(self):
        res=cv.blur(self.img,(5,5))
        return res
    def gaussian(self):
        res = cv.GaussianBlur(self.img,(5,5),0)
        return res
    def median(self):
        res = cv.medianBlur(self.img, 5)
        return res
    def unMark(self):

        '''gaussian_3 = cv.GaussianBlur(self.img, (9, 9), 10.0)
        mark=self.img-gaussian_3
        res = mark*0.5 + self.img '''
        image=self.img
        gaussian= cv.GaussianBlur(image, (9, 9), 10.0)
        res = cv.addWeighted(image, 1.5, gaussian, -0.5, 0, image)
        #res = cv.addWeighted(self.img, 1.5, gaussian_3, -0.5, 0, self.img)
        return res
    def laplacian(self):
        image=self.img
        sharpeningKernel = np.zeros((3, 3), np.float32)
        sharpeningKernel[0, 1] = 1.0
        sharpeningKernel[1, 0] = 1.0
        sharpeningKernel[1, 1] = -4.0
        sharpeningKernel[1, 2] = 1.0
        sharpeningKernel[2, 1] = 1.0
        imgfloat = image.astype(np.float32) / 255
        imgLaplacian = cv.filter2D(imgfloat, cv.CV_32F, sharpeningKernel)
        res = imgfloat - imgLaplacian
        res[res < 0.0] = 0.0
        res[res > 1.0] = 1.0

        res = (res * 255).astype(np.uint8)
        return res
    def compositeLaplacian(self):
        image = self.img
        sharpeningKernel = np.zeros((3, 3), np.float32)
        sharpeningKernel[0, 1] = -1.0
        sharpeningKernel[1, 0] = -1.0
        sharpeningKernel[1, 1] = 5.0
        sharpeningKernel[1, 2] = -1.0
        sharpeningKernel[2, 1] = -1.0
        imgfloat = image.astype(np.float32) / 255
        imgLaplacian = cv.filter2D(imgfloat, cv.CV_32F, sharpeningKernel)
        res =  imgLaplacian
        res[res < 0.0] = 0.0
        res[res > 1.0] = 1.0

        res = (res * 255).astype(np.uint8)
        return res

    def highBoost(self):
        image = self.img
        A=8.0
        sharpeningKernel = np.zeros((3, 3), np.float32)
        sharpeningKernel[0, 0] = -1.0
        sharpeningKernel[0, 1] = -1.0
        sharpeningKernel[0, 2] = -1.0
        sharpeningKernel[1, 0] = -1.0
        sharpeningKernel[1, 1] = A
        sharpeningKernel[1, 2] = -1.0
        sharpeningKernel[2, 0] = -1.0
        sharpeningKernel[2, 1] = -1.0
        sharpeningKernel[2, 2] = -1.0
        imgfloat = image.astype(np.float32) / 255
        imgHighBoost = cv.filter2D(imgfloat, cv.CV_32F, sharpeningKernel)
        res=imgfloat+imgHighBoost
        res[res < 0.0] = 0.0
        res[res > 1.0] = 1.0
        res = (res * 255).astype(np.uint8)
        return res
    def fourier(self):
        image=self.img
        imgfloat = image.astype(np.float32) / 255
        f = np.fft.fft2(imgfloat)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20 * np.log(np.abs(fshift))
        cv.imshow("ok",magnitude_spectrum)
        return magnitude_spectrum
    def highPassFilter(self):
        data = self.img.astype(np.float32) / 255
        sharpeningKernel = np.zeros((3, 3), np.float32)
        sharpeningKernel[0, 0] = -1.0
        sharpeningKernel[0, 1] = -1.0
        sharpeningKernel[0, 2] = -1.0
        sharpeningKernel[1, 0] = -1.0
        sharpeningKernel[1, 1] =  8.0
        sharpeningKernel[1, 2] = -1.0
        sharpeningKernel[2, 0] = -1.0
        sharpeningKernel[2, 1] = -1.0
        sharpeningKernel[2, 2] = -1.0

        highpass_5x5 = cv.filter2D(data, cv.CV_32F, sharpeningKernel)
        cv.imshow("x",highpass_5x5)
        return highpass_5x5
