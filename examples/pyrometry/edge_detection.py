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

contours = measure.find_contours(array=gray, level=100)

fig, ax = plt.subplots()
ax.imshow(gray, cmap=plt.cm.gray, alpha=1)

def calculate_area(countour):
    c = np.expand_dims(countour.astype(np.float32), 1)
    c = cv.UMat(c)
    
    return cv.contourArea(c)

for contour in contours:
    area = calculate_area(contour)
    
    if calculate_area(contour) > 250:
        ax.plot(contour[:, 1], contour[:, 0], linewidth=0.5, color='orangered')

ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.savefig("edge_detection_figure.png", dpi=500)
