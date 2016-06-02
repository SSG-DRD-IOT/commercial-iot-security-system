"""
arithmetic operations like addition, subtraction, bitwise operations, ...
functions:
cv2.
    add()
    addWeighted()
"""
# Image Addition

# add 2 images by OpenCV function cv2.add() or by numpy operation res = img1 + img2
#   both image of same depth and type or second image scalar value
# NOTE: diff between OpenCV and Numpy addition:
#   OpenCV addition is saturated operation
#   Numpy addition is modulo operation
x = np.uint8([250])
y = uint8([10])

print cv2.add(x,y) #250+10 = 260 => 255
print x+y # 250+10 = 260 % 256 = 4
# when adding images, OpenCV fun yields better result --> stick to OpenCV functions

# Image Blending
# different weights given to images --> feeling of transparency
# images added per eq'n
#   g(x) = (1 - /alpha)f_0(x) + /alpha * f_1(x)
#   vary /alpha 0-->1, perform cool transitions between images
# cv2.addWeighted() applies transformation on the image:
#   dst = /alpha * img1  +  /beta * img2  +  /gamma

# ex. (/gamma = 0)
img1 = cv2.imread('m1.png')
img2 = cv2.imread('opencv_logo.jpg')

# 1st img given weight of 0.7, 2nd img given 0.3
dst = cv2.addWeighted(img1, 0.7, img2, 0.3, 0)

cv2.imshow('dst', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Bitwise Operations

# includes bitwise AND, OR, NOT, XOR operations
# useful for extracting part of image, defining and working non-rectangular ROI, etc.
# ex. to change a particular part of an image

# put OpenCV logo above an image; want it to be opaque

# load 2 images
img1 = cv2.imread('messi5.jpg')
img2 = cv2.imread('opencv_logo.png')

# want to put logo on top-left corner, so create an ROI
rows, cols, channels = img2.shape
roi = img1[0:rows, 0:cols]

# create a mask of logo and create its inverse mask also
img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)
# NOTE: cv2.threshold(src_image (grayscale), threshold val used to classify pixel vals, maxVal to be given if pixel val more than threshold value, thresholding style)

# black out the area of logo in ROI
img1_bg - cv2.bitwise_and(roi, roi, mask = mask_inv)

# take only region of logo from logo image
img2_fg = cv2.bitwise_and(img2, img2, mask = mask)

# put logo in ROI and modify the main image
dst = cv2.add(img1_bg, img2_fg)
img1[0:rows, 0:cols] = dst

cv2.imshow('res', img1)
cv2.waitKey(0)
cv2.destroyAllWindows()
