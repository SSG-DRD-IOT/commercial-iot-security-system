"""
Geometric transformations of images
- translation
- rotation
- affine transformations
cv2.getPerspectiveTransform

transformation functions:
cv2.
    warpAffine - 2x3 transformation matrix input
    warpPerspective -   3x3 transformation matrix input
"""

# Scaling - resizing the image
# openCV uses cv2.resize() (manually specify size or scaling factor)
#   different interpolation methods used
#       preferable:
#         cv2.INTER_AREA
#         cv2.INTER_CUBIC (slow)
#         cv2.INTER_LINEAR (default)

# resize an input image:
import cv2
import numpy as np

img = cv2.imread('messi5.jpg')
res = cv2.resize(img, None, fx=2, fy=2, interpolation = cv2.INTER_CUBIC)

#OR
height, width = img.shape[:2]
res = cv2.resize(img, (2 * width, 2 * height), interpolation = cv2.INTER_CUBIC)

# Translation
# shifting of object's location
# if know shift in (x,y) direction, create transformation matrix M:
# M = [1 0 t_x;
#      0 1 t_y]
# make into Numpy array of type np.float32, pass into cv2.warpAffine() function

# ex. shift of (100, 50)
import cv2
import numpy as np

img = cv2.imread('messi5.jpg', 0)
rows, cols = img.shape

M = np.float32([[1, 0, 100], [0, 1, 50]])
dst = cv2.warpAffine(img, M, (cols, rows))

cv2.imshow('img', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
# WARNING: 3rd argument of cv2.warpAffine() is size of input image, of the form
# **(width, height)**
# width = # columns, height = # rows

# Rotation
# rot of image by angle /th is achieved by transformation matrix of form
# M = [cos(/th) -sin(/th);
#      sin(/th)  cos(/th)]
# BUT openCV provides scaled rotation with adjustable center of rotation to rotate any location you prefer
# Modified transformation matrix:
# M = [/alpha /beta (1-/alpha)*center.x-/beta*center.y
#      -/beta /alpha /beta*center.x+(1-/alpha)*center.y]
# where:
#     /alpha = scale * cos(/th)
#     /beta = scale * sin(/th)

# openCV provides function cv2.getRotationMatrix2D

# ex. rotate image by 90 degrees wrt center w/o any scaling
igm = cv2.imread('messi5.jpg', 0)
rows, cols = img.shape

M = cv2.getRotationMatrix2D((cols/2, rows/2), 90, 1)
dst = cv2.warpAffine(img, M, (cols, rows))

# Affine Transformations
# all parallel lines in original image are still parallel in output image
# to find transform matrix, need 3 pts from input mg & corresponding locations in output img

# cv2.getAffineTransform creates 2x3 matrix, passed to cv2.warpAffine
# NOTE: affine function = linear function + translation
# ex - select 3 pts, indicate where they will me located after transformation
img = cv2.imread('drawing.png')
rows, cols, ch = img.shape

pts1 = np.float32([50.50], [200,50], [50,200])
pts2 = np.float32([[10,100], [200,50], [100,250]])

M = cv2.getAffineTransform(pts1, pts2)

dst = cv2.warpAffine(img, M, (cols, rows))

plt.subplot(121), plt.imshow(img), plt.title('Input')
plt.subplot(122), plt.imshow(dst), plt.title('Output')
plt.show()


# Perspective Transfomation
# need 3x3 transformation matrix
# straight lines remain straight even after transformation
# need 4 pts on input image and corresponding pts on the output image
# among 4 pts, 3 should not be collinear
# cv2.getPerspectiveTransform returns the transformation matrix
# then, apply cv2.warpPerspective with 3x3 transformation matrix

img = cv2.imread('sudokusmall.png')
rows, cols, ch = img.shape

pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])

M = cv2.getPerspectiveTransform(pts1, pts2)

dst = cv2.warpPerspective(img, M, (300, 300))

plt.subplot(121), plt.imshow(img), plt.title('Input')
plt.subplot(122), plt.imshow(dst), plt.title('Output')
plt.show()

# SEE: "Computer Vision: Algorithms and Applications", Richard Szeliski
