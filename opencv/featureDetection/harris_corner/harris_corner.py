"""
Harris Corner Detection
functions:
cv2.
    cornerHarris()
    cornerSubPix()

corners - regions in image with large variation in intensity in all directions
detect by:
    find difference in intensity for a displacement of (u, v) in all directions
    E(u, v) = sum(wrt x,y) w(x, y) [I(x+u, y+v) - I(x, y)]^2
        w is window function, , I(x+u, y+v) shifted intensity, I(x, y) intensity
        window function either rect window or gaussian window (gives weights to underneath pixels)
have to maximize E(u, v) for corner detection
    -> have to maximize 2nd term
        apply taylor expansion, get

        E(u, v) ~= [u v] M [u v]'
        M = sum(wrt x, y) w(x, y) [I_x I_y] x [I_x; I_y]
        I_x and I_y are image derivs in x and y dirs, respectively
            can be found with cv2.Sobel()
After, they created a score (an eq'n) that determines if window contains corner or not
    R = det(M) - k(trace(M))^2
    det(M) = \lambda_1 * \lambda_2
    trace(M) = \lambda_1 + \lambda_2
    \lambda_1 & \lambda_2 are eigenvals of M
        values of eigenvals determine whether region is corner, edge, or flat
            when |R| small, when \lambda_1 & \lambda_2 small, region flat
            when R < 0, when \lambda_1 >> \lambda_2 or vv, region is edge
            when R large, when \lambda_1 & \lambda_2 large and \lambda_1 ~ \lambda_2, region is a corner
            see: http://docs.opencv.org/3.1.0/harris_region.jpg
Result of Harris corner detection: grayscale image with these scores
    thresholding for suitable gives corners of image
"""

# Harris Corner Detector in OpenCV
# function: cv2.cornerHarris()
# arguments:
    # img - input image; grayscale and float32 type
    # blockSize - size of nbhd considered for corner detection
    # ksize - aperture parameter of Sobel deriv used
    # k - Harris detector free parameter in eq'n

# ex.
import cv2
import numpy as np

filename = 'chessboard.png'
img = cv2.imread(filename)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)
dst = cv2.cornerHarris(gray, 2, 3, 0.04)

# result is dilated for marking the corners, not important
dst = cv2.dilate(dst, None)

# Threshold for an optimal value, it may vary depending on the image
img[dst>0.01*dst.max()] = [0, 0, 255]

cv2.imshow('dst', img)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows
