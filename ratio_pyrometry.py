import math
import cv2 as cv
import numpy as np
from numba import jit

# camera settings
I_Darkcurrent = 7.7
exposure_time = 4
f_stop = 5
ISO = 100 # basically brightness

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
            if ratio < 600 or ratio > 1200:
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

img = cv.imread('01-0001.png')

img = rg_ratio_normalize(img)
kernel = np.array([
    [0.1, 0.1, 0.1],
    [0.1, 1, 0.1],
    [0.1, 0.1, 0.1],
])
img = cv.filter2D(src=img, ddepth=-1, kernel=kernel)
# img = cv.bitwise_not(img)
img = cv.applyColorMap(img, cv.COLORMAP_JET)
cv.imwrite('01-0001-transformed-ratio.png', img)
