# MONOCHROME EDGE DETECTION

import cv2 as cv
import numpy as np
from skimage import measure, morphology, color, segmentation
import matplotlib.pyplot as plt

file = 'streaktest2.png'
img = cv.imread(file)

# blurred = cv.GaussianBlur(img, (8, 8), 0)

retval, thresh_gray = cv.threshold(img, 120, 255, cv.THRESH_BINARY)

kernel = np.ones((7, 7), np.uint8)
image = cv.morphologyEx(thresh_gray, cv.MORPH_CLOSE, kernel, iterations=1)
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

retval, gray = cv.threshold(gray, 0, 255, cv.THRESH_BINARY)

gray = cv.copyMakeBorder(
    gray, 
    20, 
    20, 
    20, 
    20, 
    cv.BORDER_CONSTANT, 
    value=0
)

# cv.imshow('gray', gray)
# cv.waitKey(0)

# contours = measure.find_contours(array=gray, level=100)
_img, contours = cv.findContours(gray, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)[0]

fig, ax = plt.subplots()
ax.imshow(gray, cmap=plt.cm.gray, alpha=1)

def calculate_area(countour):
    c = np.expand_dims(countour.astype(np.float32), 1)
    c = cv.UMat(c)

    return cv.contourArea(c)

def center_of_mass(X):
    x = X[:,0]
    y = X[:,1]
    g = (x[:-1]*y[1:] - x[1:]*y[:-1])
    A = 0.5*g.sum()
    cx = ((x[:-1] + x[1:])*g).sum()
    cy = ((y[:-1] + y[1:])*g).sum()

    return 1./(6*A)*np.array([cx,cy])


img_new = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)

for contour in contours:
    area = calculate_area(contour)

    # if area > 250:
        # cnt = np.array(contour).reshape((-1, 1, 2)).astype(np.int32)
        # cv.drawContours(img_new, [cnt], -1, (0, 200, 255), thickness=10)

    cv.drawContours(img_new, [contour], -1, (0, 200, 255), thickness=3)

        # ax.plot(contour[:, 1], contour[:, 0], linewidth=0.5, color='orangered')

# cv.imshow('contours', img_new)
# cv.waitKey(0)

cv.imwrite("firebrand_contours_opencv.png", img_new)

ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.savefig("edge_detection_figure.png", dpi=500)
