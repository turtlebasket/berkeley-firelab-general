import ratio_pyrometry

@jit(nopython=True)
def normalization_func_customizable(i, I_Darkcurrent, ISO, f_stop, exposure_time):
    return (i - I_Darkcurrent) * (f_stop ** 2) / (ISO * exposure_time)


