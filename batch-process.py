import yaml
import cv2 as cv
import numpy as np
import os
from matplotlib import pyplot as plt, image as mpimg
from ratio_pyrometry import rg_ratio_normalize

config = {}
with open("./config.yaml", "r") as yaml_stream:
    config = yaml.safe_load(yaml_stream)

img_input_dir = "images-input"
img_out_dir = "images-output"
accepted_formats = [
    ".jpg",
    ".jpeg",
    ".png",
    ".tiff",
]

files = []

for file in os.listdir(img_input_dir):
    filename = os.fsdecode(file)
    valid = False
    for fmt in accepted_formats:
        if filename.endswith(fmt):
            files.append(filename)
            valid = True
            break
    if not valid and filename != ".gitkeep":
        print(f"Invalid file extension for {filename}.")
        exit

for filename in files:
    # read image & crop
    img_orig = cv.imread(f'{img_input_dir}/{filename}', cv.IMREAD_UNCHANGED)

    img = rg_ratio_normalize(
        img_orig,
        config['i-darkcurrent'],
        config['f-stop'],
        config['exposure-time'],
        config['iso'],
        config['min-temp'],
        config['max-temp'],
        config['scaling-factor'],
        img_out=False
    )

    # build & apply smoothing conv kernel
    k = []
    smoothing_radius = config['smoothing-radius']
    for i in range(smoothing_radius):
        k.append([1/(smoothing_radius**2) for i in range(smoothing_radius)])
    kernel = np.array(k)

    img = cv.filter2D(src=img, ddepth=-1, kernel=kernel)

    # chop off alphas & reverse bgr
    img_orig = img_orig[:,:,:3]
    img_orig = img_orig[:,:,::-1]

    fig = plt.figure()
    ax = fig.add_subplot(1, 2, 1)
    ax.set_title("Original Image")
    imgplot_orig = plt.imshow(img_orig)
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.set_title("Output Heatmap")
    imgplot_final = plt.imshow(img, cmap="plasma")
    ticks = np.linspace(
        config['min-temp'], 
        config['max-temp'],
        4
    ).tolist()
    cbar = plt.colorbar(
        orientation="horizontal",
    )
    cbar.ax.set_xticklabels([str(t) for t in ticks])

    name = filename.split(".")[0]
    extension = filename.split(".")[1]
    fig.savefig(f"{img_out_dir}/{name}-transformed.{extension}", dpi=120)
