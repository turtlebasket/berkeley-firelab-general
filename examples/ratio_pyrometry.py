import math
import cv2 as cv
import numpy as np
from numba import jit
import json

# camera settings
file = '01-0001.png'
I_Darkcurrent = 150.5
exposure_time = 0.500
f_stop = 2.4
ISO = 64 # basically brightness

# pyrometry config
MAX_TEMP = 1200
MIN_TEMP = 60
# original range from paper
# MAX_GR_RATIO = 1200
# MIN_GR_RATIO = 600

# Cropping config
x1 = 420
x2 = 1200
y1 = 400
y2 = -1

# post-processing
smoothing_radius = 2

# temperature key generation
key_entries = 6


@jit(nopython=True)
def rg_ratio_normalize(imgarr):
    # set max & min to most extreme values, 
    # work up & down respectively from there
    tmin = MAX_TEMP
    tmax = 0

    imgnew = imgarr
    for i in range(len(imgarr)):
        for j in range(len(imgarr[i])):
            px = imgarr[i][j]
            r_norm = normalization_func(px[0])
            g_norm = normalization_func(px[1])

            # apply camera calibration func
            temp_C = pyrometry_calibration_formula(g_norm, r_norm)

            # remove pixels outside calibration range
            if MAX_TEMP != None and temp_C > MAX_TEMP or MIN_TEMP != None and temp_C < MIN_TEMP:
                temp_C = 0

            # update min & max
            if temp_C < tmin and temp_C >= 0:
                tmin = temp_C
            if temp_C > tmax:
                tmax = temp_C

            imgnew[i][j] = [temp_C, temp_C, temp_C]
    return imgnew, tmin, tmax


@jit(nopython=True)
def normalization_func(i):
    """
    does something to the pixels that i don't understand lol
    """
    return (i - I_Darkcurrent) * (f_stop ** 2) / (ISO * exposure_time)


@jit(nopython=True)
def pyrometry_calibration_formula(i_ng, i_nr):
    """
    Given the green-red ratio, calculates an approximate temperature 
    in Celsius.
    """
    return 362.73 * math.log10(
        (i_ng/i_nr) ** 3
    ) + 2186.7 * math.log10(
        (i_ng/i_nr) ** 2
    ) + 4466.5 * math.log10(
        (i_ng / i_nr)
    ) + 3753.5


# read image & crop
file_name = file.split(".")[0]
file_ext = file.split(".")[1]
img = cv.imread(file)
img = img[y1:y2, x1:x2]
cv.imwrite(f'{file_name}-cropped.{file_ext}', img)

# img = cv.imread('ember_test.png')

img, tmin, tmax = rg_ratio_normalize(img)

print(f"min: {tmin}°C")
print(f"max: {tmax}°C")

# build & apply smoothing conv kernel
k = []
for i in range(smoothing_radius):
    k.append([1/(smoothing_radius**2) for i in range(smoothing_radius)])
kernel = np.array(k)

img = cv.filter2D(src=img, ddepth=-1, kernel=kernel)

# write colormapped image
img_jet = cv.applyColorMap(img, cv.COLORMAP_JET)
cv.imwrite(f'{file_name}-cropped-transformed-ratio.{file_ext}', img_jet)

# --- Generate temperature key ---

# adjust max & min temps to be the same as the image
# tmin_adj = tmin / (smoothing_radius ** 2)
# tmax_adj = tmax / (smoothing_radius ** 2)
# Generate 6-step key
step = (tmax - tmin) / (key_entries-1)
temps = []
key_img_arr = [[]]
for i in range(key_entries):
    res_temp = tmin + (i * step)
    res_color = (tmax - (i * step)) / MAX_TEMP * 255
    temps.append(res_temp)
    key_img_arr[0].append([res_color, res_color, res_color])

key_img = np.array(key_img_arr).astype(np.uint8)
key_img_jet = cv.applyColorMap(key_img, cv.COLORMAP_JET)
# cv.imwrite(f'{file_name}-key.{file_ext}', key_img_jet)

tempkey = {}
for i in range(len(temps)):
    c = key_img_jet[0][i]
    tempkey[temps[i]] = f"rgb({c[0]}, {c[1]}, {c[2]})"

print(json.dumps(tempkey, indent=4))
