# MONOCHROME EDGE DETECTION

import cv2 as cv
import numpy as np

# edge-detection kernel amplification
AMPLIFIER=9

MIN_INTENSITY=100

# file = '01-0001-cropped.png'
file = 'streaktest.png'
file_name = file.split(".")[0]
file_ext = file.split(".")[1]

img = cv.imread(file)

img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

kernel = np.array([
    [-1, -1, -1],
    [-1, AMPLIFIER, -1],
    [-1, -1, -1],
])
img = cv.filter2D(src=img, ddepth=-1, kernel=kernel)

cv.imwrite(f'{file_name}-edge-detection.{file_ext}', img)
