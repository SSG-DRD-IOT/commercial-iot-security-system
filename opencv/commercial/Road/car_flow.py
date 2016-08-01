###############################################################################
# Author: Daniil Budanov
# Contact: danbudanov@gmail.com
# Summer Internship - 2016
###############################################################################
# Title: car_flow.py
# Project: Car Motion Detection
# Description:
#   uses optical flow to find car displacement vectors
#   then, uses a perspective transform to estimate car velocity
# Last Modified: 8.1.2016
###############################################################################
import cv2
import numpy as np

cap = cv2.VideoCapture("carsCrop.avi")

def ptAvg(pt1, pt2):
    ptMx = (pt1[0] + pt2[0])/2
    ptMy = (pt1[1] + pt2[1])/2
    ptM = (ptMx, ptMy)
    return ptM


def regionSelect(event, x, y, flags, param):
    global calcSDAvg, sdList, sdAvg
    if event == cv2.EVENT_LBUTTONDOWN:
        print "{}: ( {}, {} )".format(param, x, y)


# small macros
def ftps2mph(ftps):
    return ftps * 3600 / 5280.

cv2.namedWindow("road")
cv2.namedWindow("transformed")

cv2.setMouseCallback("road", regionSelect, "road")
cv2.setMouseCallback("transformed", regionSelect, "rectangle")

# road ROI corners in original frame
p00 = (210, 204)
p01 = (423, 210)
p10 = (82, 355)
p11 = (544, 356)

# # corners of perspective transform of ROI
# q00 = (0, 0)
# q01 = (250, 0)
# q10 = (0, 500)
# q11 = (250, 500)

# corners of perspective transform of ROI
q00 = (0, 0)
q01 = (350, 0)
q10 = (0, 700)
q11 = (350, 700)

# endpoints of marking on the road
m1 = (271, 236) # white markings
m2 = (275, 224)
# m1 = (262, 268) # space between markings
# m2 = (271, 235)

# float array of corners in original ROI
pts1 = np.float32([p00, p10, p11, p01])
# float array of corners in perspective transform
pts2 = np.float32([q00, q10, q11, q01])

# size of transformation
cols_t = max(pts2[:, 0])
rows_t = max(pts2[:, 1])
M = cv2.getPerspectiveTransform(pts1, pts2)

ret, frame1 = cap.read()
prev = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

rows, cols, _ = np.shape(frame1)
thresh = 3 # 5

pts = np.int32(pts1)
pts = pts.reshape((-1, 1, 2))
pts = np.array(pts)

markers = np.float32([[m1, m2]])
# print np.shape(markers)
# print markers

markers_rect = cv2.perspectiveTransform(markers, M)
# print markers_rect

markers = markers[0]
markers_rect = markers_rect[0]
marker_len = np.linalg.norm(markers_rect[0] - markers_rect[1])
# print marker_len
# real_marker_len = 10.0 # ft
real_marker_len = 5.0 # ft

print "marker length: {}".format(marker_len)
begin = True
jj = 0

fps = cap.get(cv2.CAP_PROP_FPS)
dt = 1./fps # seconds

midpt = ptAvg((0,0), (250, 500))
while(1):
    ret, frame2 = cap.read()
    jj += 1
    if ret:
        if begin:
            prev = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            begin = False
            continue

        vels_arr_i = []
        vels_arr_f = []

        transformed = cv2.warpPerspective(frame2, M, (cols_t, rows_t))

        nxt = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        if prev is nxt:
            print "same"
        #             (pyr_scale, levels, winsize, iterations, poly_n, poly_sigma, flags))
        flowParams = (  0.5,        3,       15,       3,        5,       1.2,      0)

        flow = cv2.calcOpticalFlowFarneback(prev,nxt, None, *flowParams)
        # print flow.any()
        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        # print np.max(mag)
        # print np.shape(mag)
        dispFrame = np.copy(frame2)
        cv2.line(dispFrame, m1, m2, (255, 0, 0), 2)
        goodMags = np.where(mag > thresh)
        # print np.shape(flow)
        for i, pos in enumerate(goodMags[0]):
            # if i % 160 == 0:
            if i % 20 == 0:
        # for pos in goodMags[goodMags%160]:
                y, x = (goodMags[0][i], goodMags[1][i])
                u, v = flow[y][x]
                # print "({},{}), ({}, {})".format(x, y, u, v)
                # print pos
                cv2.arrowedLine(dispFrame, (x, y), (x+int(round(u)), y+int(round(v))), (0, 0, 255), 1)
                # np.vstack((vel,  (x, y), (x+int(round(u)), y+int(round(v)))))
                vels_arr_i.append((x,y))
                vels_arr_f.append((x+u, y+v))
        vel_i = np.float32([vels_arr_i]) # array
        vel_f = np.float32([vels_arr_f])
        vel_rect_i, vel_rect_f = 0, 0

        if vel_i.any():
            # print "any"
            vel_rect_i = cv2.perspectiveTransform(vel_i, M)
            vel_rect_f = cv2.perspectiveTransform(vel_f, M)


            vel_rect_i_int = np.int32(vel_rect_i[0])
            vel_rect_f_int = np.int32(vel_rect_f[0])

            # for i in range(0, np.size(vel_rect_i) - 1):
            for i, _ in enumerate(vel_rect_i_int):
                cv2.arrowedLine(transformed, tuple(vel_rect_i_int[i,...]), tuple(vel_rect_f_int[i,...]), (0, 0, 255), 1)
            # print velMag, "\n"
            # avgMag = np.average(velMag, axis=1)
            # print "average: {}\tframe: {}".format(np.shape(avgMag), np.shape(frame2))
            # print avgMag, '\n'
        # else:
        #     print "none shape:\t", vel_i
        #     # print "not any"

        # print "i:\t{}, f:\t{}".format(np.shape(vel_rect_i), np.shape(vel_rect_f))
        # print "jj is {}".format(jj)

        # print "vi", vel_rect_i
        # print "vf", vel_rect_f

        # print np.shape(vel_rect_i)
        if type(vel_rect_i) == np.ndarray:
            # vel_rect_i_x = vel_rect_i[:, 0]
            # vel_rect_i_y = vel_rect_i[:, 1]
            # vel_rect_f_x = vel_rect_f[:, 0]
            # vel_rect_f_y = vel_rect_f[:, 1]
            vel_rect_i_x = vel_rect_i[:, :, 0]
            vel_rect_i_y = vel_rect_i[:, :, 1]
            vel_rect_f_x = vel_rect_f[:, :, 0]
            vel_rect_f_y = vel_rect_f[:, :, 1]
            # print np.shape(vel_rect_i_y)
            # print "xi: {}\nyi: {}\n xf: {}\nyf: {}".format(vel_rect_i_x, \
            #                                         vel_rect_i_y, \
            #                                         vel_rect_f_x, \
            #                                         vel_rect_f_y)
            velMag, velAng = cv2.cartToPolar(vel_rect_f_x - vel_rect_i_x,\
                                                vel_rect_f_y - vel_rect_i_y)
            # print 1
            # print jj, ":\t", 1
        else:
            # print type(vel_rect_i)
            # print "int rect i:", vel_rect_i
            # vel_rect_i_x, vel_rect_i_y, vel_rect_f_x, vel_rect_f_y = 0, 0, 0, 0
            # velMag, velAng = cv2.cartToPolar(vel_rect_f_x - vel_rect_i_x,\
                                                # vel_rect_f_y - vel_rect_i_y)
            # print "xi: {}\nyi: {}\n xf: {}\nyf: {}".format(vel_rect_i_x, \
                                                    # vel_rect_i_y, \
                                                    # vel_rect_f_x, \
                                                    # vel_rect_f_y)
            velMag = 0
            # print 0 # pattern: 110110110110110110...
            # print jj, ":\t", 0
        # velMag, velAng = cv2.cartToPolar(vel_rect_f_x - vel_rect_i_x,\
        #                                     vel_rect_f_y - vel_rect_i_y)
        # print "velmag is", np.shape(velMag)
        # print velMag, "\n"
        normer = float(np.max(mag))
        # print "normer is:", normer
        if normer:
            mag_norm = np.uint8(mag * 255 / normer)
            mag_norm = cv2.applyColorMap(mag_norm, cv2.COLORMAP_JET)
        # print np.max(velMag)
        avgMag = np.average(velMag)

        realDisp = avgMag * real_marker_len / marker_len # real-life displacement
        # print realDisp
        realSpeed = realDisp / dt # real-life speed
        realSpeed_mph = ftps2mph(realSpeed)
        if realSpeed:
            print realSpeed_mph
        # print realDisp
        cv2.polylines(dispFrame, [pts], True, (0, 255, 255))
        cv2.line(transformed, tuple(markers_rect[0]), tuple(markers_rect[1]), (255, 0, 0), 2)
        cv2.arrowedLine(transformed, midpt, (midpt[0], midpt[1]+int(avgMag)), (0, 0, 0), 2)
        cv2.imshow("road", dispFrame)
        cv2.imshow("transformed", transformed)
        if normer:
            # print np.shape(mag_norm)
            cv2.imshow("normalized magnitudes", mag_norm)
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

        prev = nxt
    else:
        break
print "done"
cap.release()
cv2.destroyAllWindows
