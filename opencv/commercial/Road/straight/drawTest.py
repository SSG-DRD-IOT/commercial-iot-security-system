from math import pi, sqrt
import numpy as np
import cv2

# img = np.zeros((200, 400))
HEIGHT = 200
WIDTH = 400
img = np.zeros((HEIGHT, WIDTH))


# diam = 447.21
ROWS, COLS = np.shape(img)
# R = max(ROWS, COLS) / min(ROWS, COLS)
# if ROWS > COLS:
#     COLS = COLS * R
# else:
#     ROWS = ROWS * R
if ROWS > COLS:
    COLS = ROWS
else:
    ROWS = COLS
print "rows: {}, cols: {}".format(ROWS, COLS)
rho = 200 / sqrt(2)
theta = pi/4
# theta = 0
# theta = pi * .1

a = np.cos(theta)
b = np.sin(theta)
x0 = a*rho
y0 = b*rho
print "a: {}, b: {}".format(a, b)


x1 = int(x0 + COLS*(-b))
y1 = int(y0 + ROWS*(a))
x2 = int(x0 - COLS*(-b))
y2 = int(y0 - ROWS*(a))

# original - works best
# x1 = int(x0 + COLS*(-b))
# y1 = int(y0 + ROWS*(a))
# x2 = int(x0 - COLS*(-b))
# y2 = int(y0 - ROWS*(a))

# mod1
# x1 = int(x0 + COLS*(b))
# y1 = int(y0 + ROWS*(a))
# x2 = int(x0 - COLS*(b))
# y2 = int(y0 - ROWS*(a))

# mod2
# x1 = int(x0 - COLS*(b))
# y1 = int(y0 + ROWS*(a))
# x2 = int(x0 + COLS*(b))
# y2 = int(y0 - ROWS*(a))

cv2.line(img, (x1, y1), (x2, y2), 255, 1)

print "(x1, y1): ({}, {}), (x2, y2): ({}, {})".format(x1, y1, x2, y2)
# print "slope = {}".format(-(float(y2)-float(y1))/(float(x2) - float(x1)))
cv2.imshow("line", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
