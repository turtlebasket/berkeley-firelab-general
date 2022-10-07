import math
import cv2 as cv
import numpy as np
from numba import jit

# camera settings
file = '01-0003.png'
I_Darkcurrent = 150.5
exposure_time = 0.5
f_stop = 2.4
ISO = 64 # basically brightness

# runtime config
MAX_GR_RATIO = 2000
MIN_GR_RATIO = None

x1 = 420
x2 = 1200
y1 = 400
y2 = -1

@jit(nopython=True)
def rg_ratio_normalize(imgarr):
    imgnew = imgarr
    for i in range(len(imgarr)):
        for j in range(len(imgarr[i])):
            px = imgarr[i][j]
            r_norm = normalization_func(px[0])
            g_norm = normalization_func(px[1])

            # apply camera calibration func
            ratio = pyrometry_calibration_formula(g_norm, r_norm)

            # remove edge cases
            if MAX_GR_RATIO != None and ratio > MAX_GR_RATIO or MIN_GR_RATIO != None and ratio < MIN_GR_RATIO:
                ratio = 0

            imgnew[i][j] = [ratio, ratio, ratio]
    return imgnew

@jit(nopython=True)
def normalization_func(i):
    return (i - I_Darkcurrent) * (f_stop ** 2) / (ISO * exposure_time)

@jit(nopython=True)
def pyrometry_calibration_formula(i_ng, i_nr):
    return 362.73 * math.log10(
        (i_ng/i_nr) ** 3
    ) + 2186.7 * math.log10(
        (i_ng/i_nr) ** 3
    ) + 4466.5 * math.log10(
        (i_ng / i_nr) ** 3
    ) + 3753.5

# read image & crop
file_name = file.split(".")[0]
file_ext = file.split(".")[1]
img = cv.imread(file)
img = img[y1:y2, x1:x2]
cv.imwrite(f'{file_name}-cropped.{file_ext}', img)

# img = cv.imread('ember_test.png')

img = rg_ratio_normalize(img)

# apply smoothing conv kernel
kernel = np.array([
    [1/2, 1/2],
    [1/2, 1/2],
])

# kernel = np.array([
#     [1/3, 1/3, 1/3],
#     [1/3, 1/3, 1/3],
#     [1/3, 1/3, 1/3],
# ])

# kernel = np.array([
#     [1/4, 1/4, 1/4, 1/4],
#     [1/4, 1/4, 1/4, 1/4],
#     [1/4, 1/4, 1/4, 1/4],
#     [1/4, 1/4, 1/4, 1/4],
# ])

# Scaling adjustment factor
kernel *= 3/5

img = cv.filter2D(src=img, ddepth=-1, kernel=kernel)

# apply jet color map
img = cv.applyColorMap(img, cv.COLORMAP_JET)

cv.imwrite(f'{file_name}-cropped-transformed-ratio.{file_ext}', img)
