import cv2
import numpy as np

def drawLines(img, lines):
    for line in lines:
        # print "drew a line!"
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + COLS*(-b))
        y1 = int(y0 + ROWS*(a))
        x2 = int(x0 - COLS*(-b))
        y2 = int(y0 - ROWS*(a))
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 1)
#
# def lineStart(event, x, y, flags, param):
#     if event == cv2.EVENT_LBUTTONUP
cv2.namedWindow("road")
# cv2.setMouseCallback('frame', lineStart)
frame = cv2.imread("roads.jpg")
ROWS, COLS, _ = np.shape(frame)
if ROWS > COLS:
    COLS = ROWS
else:
    ROWS = COLS
PROP = .2 # 0.04
mLen = int(COLS * PROP) # try 80
KER = 5 # 5
blur = cv2.GaussianBlur(frame, (KER,KER), 0)
# blur = frame
edge = cv2.Canny(blur, 128, 255)
kernel = np.ones((KER, KER))
edge = cv2.dilate(edge, kernel, iterations = 3)
# lines = cv2.HoughLines(edge, 1, np.pi/180, mLen)
# drawLines(frame, lines)

im2, contours, hierarchy = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(frame, contours, -1, 150,  3)
for i, cont in enumerate(contours):
    # print cont[::2]
    # print tuple(cont[::2][0][0])
    # if cv2.isContourConvex(cont):
    cv2.circle(frame, tuple(cont[1::2][0][0]), 3, (0, 0, 255), -1)
    leng =  cv2.arcLength(cont, closed = False)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "{}-{}".format(i, leng), tuple(cont[1::2][0][0]), font, .5, (0, 255, 0), 1, cv2.LINE_AA)

    # fit a line
    [vx,vy,x,y] = cv2.fitLine(cont, cv2.DIST_L2,0,0.01,0.01)
    lefty = int((-x*vy/vx) + y)
    righty = int(((COLS-x)*vy/vx)+y)
    cv2.line(frame,(ROWS-1,righty),(0,lefty),(0,255,0),2)

    # hull = cv2.convexHull(cont)
    # cv2.drawContours(frame, hull, -1, (0, 150, 150), 3)
    # break

print len(contours)
cv2.imshow("road", frame)
cv2.imshow("edge", edge)

# print lines

cv2.waitKey(0)
cv2.destroyAllWindows()
