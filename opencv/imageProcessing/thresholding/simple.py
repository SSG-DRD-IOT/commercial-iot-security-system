"""
Image thresholding
- simple thresholding
- adaptive thresholding
- Otsu's thresholding

functions:
cv2.
    threshold
    adaptiveThreshold
*       *       *
Simple thresholding
"""

# Simple Thresholding
# if pixel value > threshold val, -> one value (may be white)
#    otherwise assigned another (may be black)
# cv2.threshold
# arguments: source img (grayscale), threshold value used to classify pixels,
#           maxVal representing value to be given if pixel more (sometimes less) than threshold value
# different thresholding styles (4th argument):
# cv2.
#   THRESH_BINARY
#   THRESH_BINARY_INV
#   TRUNC
#   THRESH_TOZERO
#   THRESH_TOZERO_INV

# obtain 2 outputs: retval and thresholded image
img = v2.imread('gradient.png', 0)
ret, thresh1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
ret, thresh2 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
ret, thresh3 = cv2.threshold(img, 127, 255, cv2.THRESH_TRUNC)
ret, thresh4 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)
ret, thresh5 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO_INV)

titles = ['Original Image', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]

for i in xrange(6):
    plt.subplot(2, 3, i+1), plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])
    # use plt.subplot() function; check out Matplotlib docs
plt.show()
