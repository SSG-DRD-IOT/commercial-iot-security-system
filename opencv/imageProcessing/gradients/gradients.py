"""
Image Gradients

find image gradients, edges, ...
functions:
cv2.
    Sobel()
    Scharr()
    Laplacian()

Gradient filters = High-Pass filters - Sobel, Scharr, and Laplacian

Sobel and Scharr Derivatives
    Sobel operators - joint Gaussian smoothing + differentiation operation - more resistant to noise
    can specify firection of derivative to be taken, vertical or horizontal (yorder and xorder)
    can specify size of kernel by argument ksize (if ksize=-1, 3x3 Scharr filter is used; gives better results than 3x3 Sobel filter)
Laplacian Derivatives
    calculates Laplacian of image
        each (partial) derivative found using Sobel derivatives
        if ksize=1,
        kernel = [0 1  0;
                  1 -4 1
                  0  1 0]
"""

# all operators in a single diagram: (all kernels of 5x5 size, depth of output img passed -1 to get result of np.uint8 type)
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('dave.jpg', 0)

laplacian = cv2.Laplacian(img, cv2.CV_64F)
sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)

plt.subplot(2,2,1),plt.imshow(img,cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,2),plt.imshow(laplacian,cmap = 'gray')
plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,3),plt.imshow(sobelx,cmap = 'gray')
plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,4),plt.imshow(sobely,cmap = 'gray')
plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])

plt.show()


# problem: in ^, datatype is cv2.CV_8U or np.uint8
    # slight problem: B-to-W transition taken as Positive slope (has pos value) while W-to-B taken as Neg slope
        # when you convert to np.uint8, all neg slopes made 0 so you miss that edge
    # to detect both edges, better to keep output datatype to some higher forms
        # like cv2.CV_16S or cv2.CV_64F, take abs val, then convert back to cv2.CV_8U
# ex. of procedure on horizontal Sobel filter
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('box.jpg', 0)

# output dtype = cv2.CV_8U
sobelx8u = cv2.Sobel(img, cv2.CV_8U, 1, 0, ksize=5)

# output dtype = cv2.CV_64F. then, take its abs val and convert to cv2.CV_8U
sobelx64F = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
abs_sobel64f = np.abosolute(sobel64f)
sobel_8u = np.uint8(abs_sobel64f)

plt.subplot(1,3,1),plt.imshow(img,cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(1,3,2),plt.imshow(sobelx8u,cmap = 'gray')
plt.title('SOBEL CV_8U'), plt.xticks([]), plt.yticks([])
plt.subplot(1,3,3),plt.imshow(sobel_8u,cmap = 'gray')
plt.title('Sobel abs(CV_64F)'), plt.xticks([]), plt.yticks([])

plt.show()
