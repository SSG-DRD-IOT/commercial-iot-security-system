import cv2
import numpy as np

def nothing(x):
    pass

bgr_img = np.zeros((500, 300, 3), np.uint8)
hsv_img = np.copy(bgr_img)

cv2.namedWindow('BGR')
cv2.namedWindow('HSV')

cv2.createTrackbar('B', 'BGR', 0, 255, nothing)
cv2.createTrackbar('G', 'BGR', 0, 255, nothing)
cv2.createTrackbar('R', 'BGR', 0, 255, nothing)

# create trackbars for color change
cv2.createTrackbar('H', 'HSV', 0, 179, nothing)
cv2.createTrackbar('S', 'HSV', 0, 255, nothing)
cv2.createTrackbar('V', 'HSV', 0, 255, nothing)


while(1):
    cv2.imshow('BGR', bgr_img)
    cv2.imshow('HSV', hsv_img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    # get current positions of four trackbars
    r = cv2.getTrackbarPos('R', 'BGR')
    g = cv2.getTrackbarPos('G', 'BGR')
    b = cv2.getTrackbarPos('B', 'BGR')
    h = cv2.getTrackbarPos('H', 'HSV')
    s = cv2.getTrackbarPos('S', 'HSV')
    v = cv2.getTrackbarPos('V', 'HSV')
    # print r, g, b, h, s, v
    bgr_hsv = cv2.cvtColor(np.array([[[h, s, v]]], np.uint8), cv2.COLOR_HSV2BGR)
    # s = cv2.cvtColor(cv2.merge((np.array([h]), np.array([s]), np.array([v])), cv2.COLOR_HSV2BGR)

    bgr_img[:] = [b, g, r]
    hsv_img[:] = bgr_hsv
cv2.destroyAllWindows()
