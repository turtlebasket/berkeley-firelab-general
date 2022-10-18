import math

rg_value_sets = {
    "firebrand_test.png": [
        (219, 7),
        (227, 14),
        (166, 14),
        (197, 10),
        (230, 25),
        (228, 17),
        (218, 17),
        (221, 15),
        (210, 22),
        (229, 17),
    ],

    "streaktest.png": [
        (50, 11),
        (51, 12),
        (52, 10),
        (240, 115),
        (254, 127),
    ],

    "ember_orange.png": [
        (240, 147),
        (235, 102),
        (223, 103),
        (232, 103),
        (103, 34),
        (128, 47),
        (92, 27),
    ]
}

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
        return (
            362.73 * math.log10(i_ng/i_nr) ** 3 +
            2186.7 * math.log10(i_ng/i_nr) ** 2 +
            4466.5 * math.log10(i_ng / i_nr) +
            3753.5
        )
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
        # round(px[0] / px[1], 2),
        round(r_norm, 2),
        round(g_norm, 2),
        round(g_norm / r_norm, 4),
        res, 
    )

for (key, val) in rg_value_sets.items():
    print(f"\n{key}\n")
    tprint('RED', 'GREEN', 'RNORM', 'GNORM', 'G_n/R_n', 'RES TEMP')
    for rg in val:
        grtemp(rg)

# grtemp(white_hot)
# grtemp(hi)
# grtemp(med)
# grtemp(low)
# grtemp(custom)
