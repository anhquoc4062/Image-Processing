import sys
import cv2 as cv
import numpy as np


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


