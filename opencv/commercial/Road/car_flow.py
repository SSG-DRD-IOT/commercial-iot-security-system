###############################################################################
# Author: Daniil Budanov
# Contact: danbudanov@gmail.com
# Summer Internship - 2016
###############################################################################
# Title: car_flow.py
# Project: Car Speed Detection
# Description:
#   uses optical flow to find car displacement vectors
#   then, uses a perspective transform to estimate car velocity
# Last Modified: 8.2.2016
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


# conversion macro
def ftps2mph(ftps):
    return ftps * 3600 / 5280.

def trigger(info):
    print("triggered!")
    print info
cv2.namedWindow("road")
cv2.namedWindow("transformed")

cv2.setMouseCallback("road", regionSelect, "road")
cv2.setMouseCallback("transformed", regionSelect, "rectangle")

# road ROI corners in original frame
p00 = (210, 204)
p01 = (423, 210)
p10 = (82, 355)
p11 = (544, 356)

# create a controur from ROI
contour = np.array([p00, p01, p11, p10], dtype = np.int32).reshape((-1, 1, 2))

# size of transformation
cols_t = 350
rows_t = 700

# corners of perspective transform of ROI
q00 = (0, 0)
q01 = (cols_t, 0)
q10 = (0, rows_t)
q11 = (cols_t, rows_t)

# endpoints of dash on the road
m1 = (271, 236)
m2 = (275, 224)

# float array of corners in original ROI
pts1 = np.float32([p00, p10, p11, p01])
# float array of corners in perspective transform
pts2 = np.float32([q00, q10, q11, q01])

# generate perspective transform matrix from ROI
M = cv2.getPerspectiveTransform(pts1, pts2)

# retrieve first frame
ret, frame1 = cap.read()
rows, cols, _ = np.shape(frame1)


# optical flow operates in grayscale
prev = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

# set threshold for velocity
thresh = 3 # 5

# create ROI corners into array so that its edges can be drawn with polylines
pts = np.int32(pts1)
pts = pts.reshape((-1, 1, 2))
pts = np.array(pts)

# form dash endpoints into an array
markers = np.float32([[m1, m2]])
# perform perspective transform on dash marker points
markers_rect = cv2.perspectiveTransform(markers, M)
# remove extra layer put on markers by transform
markers_rect = markers_rect[0]
# find length of markers in rectangular space
marker_len = np.linalg.norm(markers_rect[0] - markers_rect[1])
# real-world length of markers
real_marker_len = 5.0 # ft

# beginning step; included because it can be useful for starting real-time view
begin = True
# simple counter for debug purposes
jj = 0

# get video framerate
fps = cap.get(cv2.CAP_PROP_FPS)
# calculate time interval between frames; use for velocity calculation
dt = 1./fps # seconds

# midpoint of projection frame
midpt = ptAvg((0,0), (cols_t, rows_t))

# work with every Nth displacement vector
SHOW_EVERY = 20

# main loop
while(1):
    ret, frame2 = cap.read()
    jj += 1
    if ret:
        if begin:
            # if this is the very first frame, calculate prev and continue
            # use this step for implementing inter-frame timing later on
            prev = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            begin = False
            continue
        # initial and final points of displacement vectors
        disp_arr_i = []
        disp_arr_f = []

        # warp ROI into rectangular space by applying perspective transform
        transformed = cv2.warpPerspective(frame2, M, (cols_t, rows_t))

        # perform color conversion for optical flow
        nxt = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # set optical flow parameters:
        #             (pyr_scale, levels, winsize, iterations, poly_n, poly_sigma, flags))
        flowParams = (  0.5,        3,       15,       3,        5,       1.2,      0)

        # calculate optical flow
        # yields rows x cols x 2 array with x and y components of displacement vector
        flow = cv2.calcOpticalFlowFarneback(prev,nxt, None, *flowParams)

        # calculate magnitude of displacement vector
        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])

        # create a copy of original frame on which you draw vectors
        viewFrame = np.copy(frame2)

        # draw blue line along selected dash on highway
        cv2.line(viewFrame, m1, m2, (255, 0, 0), 2)

        # find locations where displacement magnitudes surpass threshold
        goodMags = np.where(mag > thresh)

        for i, pos in enumerate(goodMags[0]):
            # to reduce quantity of vecs working with, use every SHOW_EVERY-eth vector
            if (i % SHOW_EVERY == 0):
                # get position of vector
                x, y = (goodMags[1][i], goodMags[0][i])
                if cv2.pointPolygonTest(contour,(x,y),False)==1:
                    # get horizontal and vertical components of vector
                    u, v = flow[y][x]

                    # draw the displacement vector
                    cv2.arrowedLine(viewFrame, (x, y), (x+int(round(u)), y+int(round(v))), (0, 0, 255), 1)

                    # add displacement vector initial and final points to list
                    disp_arr_i.append((x,y))
                    disp_arr_f.append((x+u, y+v))
        # make lists into numpy arrays that can be operated on
        disp_i = np.float32([disp_arr_i])
        disp_f = np.float32([disp_arr_f])

        # set rectangular displacements to 0 by default
        disp_rect_i, disp_rect_f = 0, 0

        # check if displacement vector array has any points in it
        if disp_i.any():
            # apply perspective transform on displacement vector start/end points
            disp_rect_i = cv2.perspectiveTransform(disp_i, M)
            disp_rect_f = cv2.perspectiveTransform(disp_f, M)

            # cast transformed vectors to integers in order to draw them
            disp_rect_i_int = np.int32(disp_rect_i[0])
            disp_rect_f_int = np.int32(disp_rect_f[0])

            # draw displacement vectors in rectangular space
            for i, _ in enumerate(disp_rect_i_int):
                cv2.arrowedLine(transformed, tuple(disp_rect_i_int[i,...]), tuple(disp_rect_f_int[i,...]), (0, 0, 255), 1)

        if type(disp_rect_i) == np.ndarray:
            # otherwise, 0 is returned
            # find x, y components of rectangular displacement vectors
            disp_rect_i_x = disp_rect_i[:, :, 0]
            disp_rect_i_y = disp_rect_i[:, :, 1]
            disp_rect_f_x = disp_rect_f[:, :, 0]
            disp_rect_f_y = disp_rect_f[:, :, 1]
            # find magnitudes of displacement vectors in rectangular space
            dispMag, velAng = cv2.cartToPolar(disp_rect_f_x - disp_rect_i_x,\
                                                disp_rect_f_y - disp_rect_i_y)

        else:
            # otherwise, set displacement magnitude to 0
            dispMag = 0

        # normalize magnitude map
        # can later use this for binary mapping
        normer = float(np.max(mag))
        if normer: # checks that normer is not 0
            # normalize mag
            mag_norm = np.uint8(mag * 255 / normer)
            mag_norm = cv2.applyColorMap(mag_norm, cv2.COLORMAP_JET)
        # find average displacement magnitude
        avgMag = np.average(dispMag)

        # using the [known] dash length, convert displacements to real-world distances
        # nowmalize the displacement relative to dashes and multiply by real-world dash length
        realDisp = avgMag * real_marker_len / marker_len

        # find real-world speed by dividing displacement by time interval between frames
        realSpeed = realDisp / dt # real-life speed
        # convert speed into miles per hour
        realSpeed_mph = ftps2mph(realSpeed)
        # if the real speed isn't 0, print it
        if realSpeed:
            print realSpeed_mph
            triggerInfo = {
                "event": "VehicleSpeed",
                "speed": realSpeed_mph,
                "timestamp": "3:30-5-6-17",
                "speeding": True
            }
            # trigger(triggerInfo)

        # draw the ROI boundary in yellow
        # cv2.polylines(viewFrame, [pts], True, (0, 255, 255))
        cv2.drawContours(viewFrame, [contour], 0, (0, 255, 255), 1)

        # draw line on the dashes in the rectqngular space
        cv2.line(transformed, tuple(markers_rect[0]), tuple(markers_rect[1]), (255, 0, 0), 2)

        # draw black line down middle of rectangular space showing length of average vector
        # cv2.arrowedLine(transformed, midpt, (midpt[0], midpt[1]+int(avgMag)), (0, 0, 0), 2)

        # show road with marked ROI
        cv2.imshow("road", viewFrame)
        # show rectanguler space
        cv2.imshow("transformed", transformed)

        # # for debugging
        # # show ROI mask
        # cv2.imshow("ROI Mask", roi_mask)

        if normer:
            # show region with normalized magnitudes
            cv2.imshow("normalized magnitudes", mag_norm)

        # if user presses ESC then exit
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

        # previously new gray frame becomes old one
        prev = nxt

    else:
        # if no more frames are returned from video than end video capture
        break

print "done"

# release video capture and destroy windows
cap.release()
cv2.destroyAllWindows
