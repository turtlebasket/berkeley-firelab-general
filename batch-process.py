import yaml
import cv2 as cv
import numpy as np
import os
from ratio_pyrometry import rg_ratio_normalize

config = {}
with open("./config.yaml", "r") as yaml_stream:
    config = yaml.safe_load(yaml_stream)

img_in_dir = "./images-input"
img_out_dir = "./images-output"
accepted_formats = [
    ".jpg",
    ".jpeg",
    ".png",
    ".tiff",
]

files = []

for file in os.listdir(img_in_dir):
    filename = os.fsdecode(file)
    valid = False
    for fmt in accepted_formats:
        if filename.endswith(fmt):
            files.append(os.path.join(img_in_dir, filename))
            valid = True
            break
    if not valid:
        print(f"Invalid file extension for {filename}.")
        exit
    
for filename in files:
    with open(filename) as imgfile:
        # read image & crop
        img_orig = cv.imread(imgfile, cv.IMREAD_UNCHANGED)

        img = rg_ratio_normalize(
            img_orig,
            config['i-darkcurrent'],
            config['f-stop'],
            config['exposure-time'],
            config['iso'],
            config['min-temp'],
            config['max-temp'],
            config['scaling-factor'],
        )

        # build & apply smoothing conv kernel
        k = []
        smoothing_radius = config['smoothing-radius']
        for i in range(smoothing_radius):
            k.append([1/(smoothing_radius**2) for i in range(smoothing_radius)])
        kernel = np.array(k)

        img = cv.filter2D(src=img, ddepth=-1, kernel=kernel)

        # write colormapped image
        img_jet = cv.applyColorMap(img, cv.COLORMAP_JET)

        # TODO: GENERTE TEMP KEY & OUTPUT MATPLOTLIB
