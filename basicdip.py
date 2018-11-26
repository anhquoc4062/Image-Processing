import sys
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
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
        #self.img = cv.cvtColor(self.img, cv.COLOR_BGR2RGB)

    #chuong 3
    def original(self):
        return self.img

    def negative(self):
        res = ~self.img
        return res

    def histogram(self):
        img_yuv = cv.cvtColor(self.img_original, cv.COLOR_RGB2YUV)
        img_yuv[:, :, 0] = cv.equalizeHist(img_yuv[:, :, 0])
        res = cv.cvtColor(img_yuv, cv.COLOR_YUV2RGB)
        return res

    def log(self, thresh):
        res_1 = np.uint8(np.log(self.img))
        res_2 = cv.threshold(res_1, thresh, 255, cv.THRESH_BINARY)[1]
        return res_2

    #chuong 2
    def scaling(self, size):
        res = cv.resize(self.img, None, fx = size*0.01, fy = size*0.01, interpolation = cv.INTER_CUBIC)
        return res

    def translation(self, x, y):
        rows, cols, steps = self.img.shape
        M = np.float32([[1, 0, x], [0, 1, y]])
        res = cv.warpAffine(self.img, M, (cols, rows))
        return res

    def rotation(self, angle):
        rows, cols,  steps = self.img.shape
        M = cv.getRotationMatrix2D((cols / 2, rows / 2), 360 - angle, 1)
        res = cv.warpAffine(self.img, M, (cols, rows))
        return res

    def affine(self, m):
        rows, cols, ch = self.img.shape

        pts1 = np.float32([[50, m], [200, 50], [50, 200]])
        pts2 = np.float32([[10, 100], [200, 50], [100, 250]])

        M = cv.getAffineTransform(pts1, pts2)

        res = cv.warpAffine(self.img, M, (cols, rows))
        return res

    #Chương 3

    def avg(self, m):
        res=cv.blur(self.img,(m,m))
        return res
    def gaussian(self, m):
        res = cv.GaussianBlur(self.img,(m, m),0)
        return res
    def median(self, size):
        res = cv.medianBlur(self.img, size)
        return res
    def unMark(self):
        tmp=self.img
        #image=self.img
        gaussian= cv.GaussianBlur(tmp, (9, 9), 10.0)

        res = cv.addWeighted(tmp, 1.5, gaussian, -0.5, 0.5,tmp)
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

    def highBoost(self, A):
        image = self.img
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

    #chương 5
    def fourier(self):

        img_gray = cv.cvtColor(self.img, cv.COLOR_RGB2GRAY)
        f = np.fft.fft2(img_gray)
        fshift = np.fft.fftshift(f)
        print(1)
        magnitude_spectrum = 20 * np.log(np.abs(fshift))
        print(2)
        #magnitude_spectrum = magnitude_spectrum.astype(np.uint8)
        print(3)
        cv.imshow("x", magnitude_spectrum)
        #return magnitude_spectrum

    def highPassGaussian(self):
        data = np.array(self.img, dtype=float)
        lowpass = ndimage.gaussian_filter(data, 3)
        gauss_highpass = data - lowpass
        gauss_highpass = np.uint8(gauss_highpass)
        gauss_highpass = ~gauss_highpass
        return gauss_highpass

    #chương 8
    def Canny(self):
        image = cv.cvtColor(self.img_original, cv.COLOR_BGR2GRAY)
        res = cv.Canny(image, 100, 200)
        return res

    #chương 7
    def dilate(self):
        kernel = np.ones((2, 6), np.uint8)
        res = cv.dilate(self.img, kernel, iterations=1)
        return res

    def erode(self):
        kernel = np.ones((4, 7), np.uint8)
        res = cv.erode(self.img, kernel, iterations=1)
        return res

    def open(self):
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (9, 9))
        res = cv.morphologyEx(self.img, cv.MORPH_OPEN, kernel)
        return res

    def close(self):
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (9, 9))
        res = cv.morphologyEx(self.img, cv.MORPH_CLOSE, kernel)
        return res

    # Lỗi
    def hitmis(self):
        kernel = np.array(([0, 1, 0], [1, -1, 1], [0, 1, 0]))
        res = cv.morphologyEx(self.img, cv.MORPH_HITMISS, kernel)
        return res

    def gradient(self):
        kernel = np.ones((5, 5), np.uint8)
        res = cv.morphologyEx(self.img, cv.MORPH_GRADIENT, kernel)
        return res

    def morboundary(self):
        se = np.ones((3, 3), np.uint8)
        e1 = self.img - cv.erode(self.img, se, iterations=1)
        res = e1
        return res

    def convex(self):
        self.img = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        blur = cv.blur(self.img, (3, 3))
        ret, thresh = cv.threshold(blur, 50, 255, cv.THRESH_BINARY)

        im2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        hull = []

        # calculate points for each contour
        for i in range(len(contours)):
            # creating convex hull object for each contour
            hull.append(cv.convexHull(contours[i], False))

        # create an empty black image
        res = np.zeros((thresh.shape[0], thresh.shape[1], 3), np.uint8)

        # draw contours and hull points
        for i in range(len(contours)):
            color_contours = (0, 255, 0)  # green - color for contours
            color = (255, 0, 0)  # blue - color for convex hull
            # draw ith contour
            # cv2.drawContours( self.image, contours, i, color_contours, 1, 8, hierarchy)
            # draw ith convex hull object
            cv.drawContours(res, hull, i, color, 1, 8)
        return res

    #Chương 8
    def sobelX(self):
        sobelImgX = cv.Sobel(self.img, cv.CV_8U, 1, 0, ksize=7)
        return sobelImgX

    def sobelY(self):
        sobelImgY = cv.Sobel(self.img, cv.CV_8U, 0, 1, ksize=5)
        return sobelImgY

    def lapcian(self):
        lapcian = cv.Laplacian(self.img, cv.CV_8U)
        return lapcian
