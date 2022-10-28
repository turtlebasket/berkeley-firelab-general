import cv2 as cv
import numpy as np
from skimage import measure, morphology, color, segmentation
import matplotlib.pyplot as plt

file = 'proj-area-3.jpg'

original = cv.imread(file)
original = cv.cvtColor(original, cv.COLOR_BGR2RGB)
img = original

img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

retval, thresh_gray = cv.threshold(img, 200, 255, cv.THRESH_BINARY)

def remove_dirt(image):
    image = morphology.area_closing(image, area_threshold=250, connectivity=1)
    # image = morphology.opening(image, morphology.square(5))

    return image

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

img = remove_dirt(thresh_gray)


# alpha = 1 # Contrast control (1.0-3.0)
# beta = 1 # Brightness control (0-100)

# img = cv.convertScaleAbs(img, alpha=alpha, beta=beta)

# img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# img = cv.medianBlur(img, 5)

# retval, thresh_gray = cv.threshold(img, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)


# img = cv.medianBlur(img, 5)

# img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 51, 15)

contours = measure.find_contours(array=img, level=100)

fig, ax = plt.subplots()
ax.imshow(img, cmap=plt.cm.gray, alpha=0)

index = 1

for contour in contours:
    if calculate_area(contour) > 300:
        ax.plot(contour[:, 1], contour[:, 0], linewidth=0.5, color='orangered')

        cX, cY = center_of_mass(contour)

        plt.text(cY, cX, index, color='black', fontsize=6)

        index += 1

ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])

plt.savefig('output.png', dpi=300)

# cv.imwrite('proj-area-1-processed.jpg', remove_dirt(img))