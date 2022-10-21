import math
from multiprocessing.sharedctypes import Value
import cv2 as cv
import numpy as np
from numba import jit

@jit(nopython=True)
def rg_ratio_normalize(
    imgarr, 
    I_Darkcurrent,
    f_stop, 
    exposure_time, 
    ISO, 
    MIN_TEMP, 
    MAX_TEMP,
    eqn_scaling_factor
):
    # copy image into new array & chop off alpha values (if applicable)
    imgnew = imgarr.copy()[:,:,:3]

    for i in range(len(imgarr)):
        for j in range(len(imgarr[i])):
            px = imgarr[i][j]

            # normalize R & G pixels
            g_norm = (px[1] - I_Darkcurrent) * (f_stop ** 2) / (ISO * exposure_time)
            r_norm = (px[2] - I_Darkcurrent) * (f_stop ** 2) / (ISO * exposure_time)

            # apply camera calibration func
            temp_C = pyrometry_calibration_formula(g_norm, r_norm, default=MIN_TEMP) * eqn_scaling_factor

            # remove pixels outside calibration range
            if (MIN_TEMP != None and temp_C < MIN_TEMP) or (MAX_TEMP != None and temp_C > MAX_TEMP):
                temp_C = MIN_TEMP

            # scale light intensity to calculated temperature
            pix_i = scale_temp(temp_C, MIN_TEMP, MAX_TEMP)
            imgnew[i][j] = [pix_i, pix_i, pix_i]

    return imgnew


@jit(nopython=True)
def pyrometry_calibration_formula(i_ng, i_nr, default=24.0):
    """
    Given the green-red ratio, calculates an approximate temperature 
    in Celsius. Defaults to room temperature if there's an error.
    """
    try:
        return (
            (362.73 * math.log10(i_ng / i_nr) ** 3) +
            (2186.7 * math.log10(i_ng / i_nr) ** 2) +
            (4466.5 * math.log10(i_ng / i_nr)) +
            3753.5
        )
    except:
        return default


@jit(nopython=True)
def scale_temp(t, min, max):
    """
    Scale pixel temperature (t) to light intensity given min & max temp.
    """
    return (t - min) / (max - min) * 255


def ratio_pyrometry_pipeline(
    file_bytes,
    # camera settings
    I_Darkcurrent: float,
    exposure_time: float,
    f_stop: float,
    ISO: float,
    # pyrometry config
    MAX_TEMP: float,
    MIN_TEMP: float,
    smoothing_radius: int,
    key_entries: int,
    eqn_scaling_factor: float,
):

    # read image & crop
    img_orig = cv.imdecode(file_bytes, cv.IMREAD_UNCHANGED)

    img = rg_ratio_normalize(
        img_orig,
        I_Darkcurrent,
        f_stop,
        exposure_time,
        ISO,
        MIN_TEMP,
        MAX_TEMP,
        eqn_scaling_factor
    )

    # build & apply smoothing conv kernel
    k = []
    for i in range(smoothing_radius):
        k.append([1/(smoothing_radius**2) for i in range(smoothing_radius)])
    kernel = np.array(k)

    img = cv.filter2D(src=img, ddepth=-1, kernel=kernel)

    # write colormapped image
    # img_jet = img
    img_jet = cv.applyColorMap(img, cv.COLORMAP_JET)

    # --- Generate temperature key ---

    # Generate key
    step = (MAX_TEMP - MIN_TEMP) / (key_entries-1)
    temps = []
    key_img_arr = [[]]
    for i in range(key_entries):
        res_temp = MIN_TEMP + (i * step)
        res_color = scale_temp(res_temp, MIN_TEMP, MAX_TEMP)
        temps.append(math.floor(res_temp))
        key_img_arr[0].append([res_color, res_color, res_color])

    key_img = np.array(key_img_arr).astype(np.uint8)
    key_img_jet = cv.applyColorMap(key_img, cv.COLORMAP_JET)

    tempkey = {}
    for i in range(len(temps)):
        c = key_img_jet[0][i]
        tempkey[temps[i]] = f"rgb({c[2]}, {c[1]}, {c[0]})"

    # original, transformed, legend
    return img_orig, img_jet, tempkey
