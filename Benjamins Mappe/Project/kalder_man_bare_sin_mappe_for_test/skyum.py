import cv2 as cv
import numpy as np

# Load the YUV image

image = cv.imread('Benjamins Mappe\Project\kalder_man_bare_sin_mappe_for_test\skyum.png')


height, width, channels = image.shape

# Traverse through every pixel
for y in range(height):
    for x in range(width):
        # Access the pixel value (BGR format)
        blue, green, red = image[y, x].astype(np.int32) 
        together = (blue + green + red)/3

        if (together<=200):
            image[y, x] = [0, 0, 0]

#cv.imwrite('modified_image.jpg', image)

cv.imshow('RGB Image', image)

cv.waitKey(0)
cv.destroyAllWindows()
