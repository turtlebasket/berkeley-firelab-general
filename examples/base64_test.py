import base64
import cv2 as cv

img = cv.imread('01-0001-cropped.png')

print(img[0:100])

# print(base64.b64encode(img).decode()[0:5_000])
