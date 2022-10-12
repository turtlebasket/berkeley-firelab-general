# MONOCHROME EDGE DETECTION

import cv2 as cv
import numpy as np

file = '01-0001-cropped.png'
file_name = file.split(".")[0]
file_ext = file.split(".")[1]

img = cv.imread(file)

img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

kernel = np.array([
    [-1, -1, -1],
    [-1, 8, -1],
    [-1, -1, -1],
])
img = cv.filter2D(src=img, ddepth=-1, kernel=kernel)

cv.imwrite(f'{file_name}-edge-detection.{file_ext}', img)
