import cv2
import numpy as np
cap = cv2.VideoCapture("cars.avi")

ret, frame1 = cap.read()
prev = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
# hsv = np.zeros_like(frame1)
# hsv[..., 1] = 255

thresh = 5

while(ret):
    ret, frame2 = cap.read()
    nxt = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # cv2.calcOpticalFlowFarneback(prev, next, flow, pyr_scale, levels, winsize, iterations, poly_n, poly_sigma, flags) -> flow
    #             (pyr_scale, levels, winsize, iterations, poly_n, poly_sigma, flags))
    # flowParams = (0.5,          3,       15,       3,        5,       1.2,      0) # default
    flowParams = (0.5,          3,       15,       3,        5,       1.2,      0)

    flow = cv2.calcOpticalFlowFarneback(prev,nxt, None, *flowParams)
    # print np.shape(flow)

    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    # hsv[...,0] = ang*180/np.pi/2
    # hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    # bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
    # bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

    goodMags = np.where(mag > thresh)
    for i, pos in enumerate(goodMags[0]):
        if i % 40 == 0:
            y, x = (goodMags[0][i], goodMags[1][i])
            u, v = flow[y][x]
        # print u, v
        cv2.arrowedLine(frame2, (x, y), (x+int(u), y+int(v)), (0, 255, 0), 1)
    cv2.imshow("frame2", frame2)
    # cv2.imshow('frame2',bgr)

    k = cv2.waitKey(1) & 0xff # 30
    if k == 27:
        break
    elif k == ord('s'):
        print "saved"
        # cv2.imwrite('opticalfb.png',frame2)
        # cv2.imwrite('opticalhsv.png',bgr)
    prev = nxt

cap.release()
cv2.destroyAllWindows
