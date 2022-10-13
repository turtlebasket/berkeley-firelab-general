# R & G values taken from images
import math


# Values
white_hot = (255, 255)
hi = (168, 55)
med = (146, 26)
low = (25, 4)


# Settings
I_Darkcurrent = 7.7
exposure_time = 0.500
f_stop = 2.4
ISO = 100 # basically brightness

def pyrometry_calibration_formula(i_ng, i_nr):
    """
    Given the green-red ratio, calculates an approximate temperature 
    in Celsius. 
    """
    try:
        return 362.73 * math.log10(
            (i_ng/i_nr) ** 3
        ) + 2186.7 * math.log10(
            (i_ng/i_nr) ** 2
        ) + 4466.5 * math.log10(
            (i_ng / i_nr)
        ) + 3753.5
        # return 362.73 * math.log10(
        #     (i_ng/i_nr) ** 3
        # ) + 2186.7 * math.log10(
        #     (i_ng/i_nr) ** 2
        # ) + 4466.5 * math.log10(
        #     (i_ng / i_nr)
        # ) + 3753.5
    except:
        return 'dropped'


def tprint(*items):
    for item in items:
        print(item, end="\t")
    print()


def grtemp(px):
    r_norm = (px[0] - I_Darkcurrent) * (f_stop ** 2) / (ISO * exposure_time)
    g_norm = (px[1] - I_Darkcurrent) * (f_stop ** 2) / (ISO * exposure_time)
    res = pyrometry_calibration_formula(g_norm, r_norm)
    tprint(
        px[0], 
        px[1], 
        round(px[0] / px[1], 2),
        round(r_norm, 2),
        round(g_norm, 2),
        round(r_norm / g_norm),
        res, 
    )


tprint('RED', 'GREEN', 'RATIO', 'RNORM', 'GNORM', 'NRATIO', 'RES TEMP')
grtemp(white_hot)
grtemp(hi)
grtemp(med)
grtemp(low)
