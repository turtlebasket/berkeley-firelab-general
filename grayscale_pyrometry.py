import cv2 as cv
import numpy as np

img = cv.imread('01-0001.png', 0)
kernel = np.array([
    [0.1, 0.1, 0.1],
    [0.1, 1, 0.1],
    [0.1, 0.1, 0.1],
])
img = cv.filter2D(src=img, ddepth=-1, kernel=kernel)
img = cv.applyColorMap(img, cv.COLORMAP_JET)
cv.imwrite('01-0001-transformed-grayscale.png', img)
