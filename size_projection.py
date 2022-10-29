# use headless backend
import matplotlib
matplotlib.use("Agg")

import base64
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from skimage import measure, morphology, color, segmentation
import io

def get_projected_area(image, area_threshold, display_threshold):
    total_px = image.size
    total_mm = 60322.46

    output = []
    original = cv.imdecode(image, cv.IMREAD_UNCHANGED)
    original = cv.cvtColor(original, cv.COLOR_BGR2RGB)

    img = cv.cvtColor(original, cv.COLOR_BGR2GRAY)
    _retval, thresh_gray = cv.threshold(img, 200, 255, cv.THRESH_BINARY)

    img = morphology.area_closing(thresh_gray, area_threshold=area_threshold, connectivity=1)

    contours = measure.find_contours(image=img, level=100)

    fig, ax = plt.subplots()
    ax.imshow(original, cmap=plt.cm.gray, alpha=0.3)

    index = 1

    for contour in contours:
        area = calculate_area(contour)
        
        if calculate_area(contour) > display_threshold:
            ax.plot(contour[:, 1], contour[:, 0], linewidth=0.5, color='orangered')

            cX, cY = center_of_mass(contour)
            plt.text(cY, cX, index, color='black', fontsize=6)
            
            output.append((index, round(area / total_px * total_mm, 2)))

            # print(area, total_px)


            index += 1

    ax.axis('image')
    ax.set_xticks([])
    ax.set_yticks([])
    
    ax.margins(0)

    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='png', dpi=500, bbox_inches='tight')
    my_stringIObytes.seek(0)
    image_arr = base64.b64encode(my_stringIObytes.read()).decode(encoding='utf-8')

    return image_arr, output

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
