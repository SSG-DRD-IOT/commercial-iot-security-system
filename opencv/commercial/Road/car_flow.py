import cv2
import numpy as np
cap = cv2.VideoCapture("cars.avi")

ret, frame1 = cap.read()
prev = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

rows, cols, _ = np.shape(frame1)
thresh = 1 # 5
bottomClear = 0
topCrop = int(.2*rows)

while(1):
    ret, frame2 = cap.read()
    # frame2 = frame2[topCrop:rows-1, :, :]
    # cv2.imshow('test',frame2)

    if ret:
        nxt = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # cv2.calcOpticalFlowFarneback(prev, next, flow, pyr_scale, levels, winsize, iterations, poly_n, poly_sigma, flags) -> flow
        #             (pyr_scale, levels, winsize, iterations, poly_n, poly_sigma, flags))
        flowParams = (  0.5,        3,       15,       3,        5,       1.2,      0)

        flow = cv2.calcOpticalFlowFarneback(prev,nxt, None, *flowParams)

        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])

        dispFrame = np.copy(frame2)

        goodMags = np.where(mag > thresh)

        for i, pos in enumerate(goodMags[0]):

            if i % 160 == 0:

                y, x = (goodMags[0][i], goodMags[1][i])
                u, v = flow[y][x]

                if y+v < rows - bottomClear:

                    cv2.arrowedLine(dispFrame, (x, y), (x+int(round(u)), y+int(round(v))), (0, 0, 255), 1)

        cv2.imshow("frame2", dispFrame)

        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

        prev = nxt
    else:
        break
print "done"
cap.release()
cv2.destroyAllWindows
