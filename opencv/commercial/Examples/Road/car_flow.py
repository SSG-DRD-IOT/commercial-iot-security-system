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
# Last Modified: 8.3.2016
###############################################################################
import cv2
import numpy as np
import pickle
import selectionTools
import transformTools
import utils

# load in pickled point data
fname_l = utils.inputParams

with open(fname_l, 'rb') as handle:
    pointContainer = pickle.load(handle)


# conversion macro
def ftps2mph(ftps):
    return ftps * 3600 / 5280.


cv2.namedWindow("road")
cv2.namedWindow("transformed")


# road ROI corners in original frame
p00 = pointContainer["p00"]
p01 = pointContainer["p01"]
p10 = pointContainer["p10"]
p11 = pointContainer["p11"]

# endpoints of dash on the road
m1 = pointContainer["m1"]
m2 = pointContainer["m2"]

# begin video capture
cap = cv2.VideoCapture(utils.dest)

# Defaults

# Intel blue
color_IntelBlue = (246, 141, 0)

# size of transformation
cols_t = 350
rows_t = 700

# corners of perspective transform of ROI
q00 = (0, 0)
q01 = (cols_t, 0)
q10 = (0, rows_t)
q11 = (cols_t, rows_t)

M, markers_rect, marker_len, contour = transformTools.transformedParams(p00, p10, p11, p01, m1, m2, q00, q10, q11, q01)

# real-world length of markers
real_marker_len = 5.0 # ft



# beginning step; included because it can be useful for starting real-time view
begin = True
first_video_frame = True

# frame counter for video reference
frameCount = 0
lastStart = 0

# get video framerate
fps = cap.get(cv2.CAP_PROP_FPS)
# calculate time interval between frames; use for velocity calculation
dt = 1./fps # seconds

# work with every Nth displacement vector
SHOW_EVERY = utils.vecDiv

# maximum speed over which Speeding is triggered
max_speed = 65 # mph

# main loop
while(1):
    ret, frame = cap.read()
    if ret:
        if begin:
            # if this is the very first frame, calculate prev and continue
            # use this step for implementing inter-frame timing later on
            prev = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            begin = False
            continue


        # warp ROI into rectangular space by applying perspective transform
        transformed = cv2.warpPerspective(frame, M, (cols_t, rows_t))

        # perform color conversion for optical flow
        nxt = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # set optical flow parameters:
        #             (pyr_scale, levels, winsize, iterations, poly_n, poly_sigma, flags))
        flowParams = (  0.5,        3,       15,       3,        5,       1.2,      0)

        # calculate optical flow
        # yields rows x cols x 2 array with x and y components of displacement vector
        flow = cv2.calcOpticalFlowFarneback(prev,nxt, None, *flowParams)

        # calculate magnitude of displacement vector
        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])

        # create a copy of original frame on which you draw vectors
        viewFrame = np.copy(frame)

        # draw blue line along selected dash on highway
        cv2.line(viewFrame, m1, m2, (255, 0, 0), 2)

        # find locations where displacement magnitudes surpass threshold
        goodMags = np.where(mag > utils.x_thresh)

        # initial and final points of displacement vectors
        disp_arr_i = []
        disp_arr_f = []

        for i, _ in enumerate(goodMags[0]):
            # to reduce quantity of vecs working with, use every SHOW_EVERY-eth vector
            if (i % SHOW_EVERY == 0):
                # get position of vector
                x, y = (goodMags[1][i], goodMags[0][i])
                if cv2.pointPolygonTest(contour,(x,y),False)==1:
                    # get horizontal and vertical components of vector
                    u, v = flow[y][x]

                    # draw the displacement vector
                    cv2.arrowedLine(viewFrame, (x, y), (x+int(round(u)), y+int(round(v))), color_IntelBlue, 2)

                    # add displacement vector initial and final points to list
                    disp_arr_i.append((x,y))
                    disp_arr_f.append((x+u, y+v))
        # make lists into numpy arrays that can be operated on
        disp_i = np.float32([disp_arr_i])
        disp_f = np.float32([disp_arr_f])



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
                cv2.arrowedLine(transformed, tuple(disp_rect_i_int[i,...]), tuple(disp_rect_f_int[i,...]), color_IntelBlue, 2)

        # if type(disp_rect_i) == np.ndarray:
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

            if utils.debug:
                print realSpeed_mph
            if realSpeed_mph > max_speed:
                print "speeding at:", realSpeed_mph, "mph"
                lastStart = frameCount
                if utils.record and first_video_frame:
                    # create the VideoWriter object
                    fourcc = cv2.VideoWriter_fourcc(*'MJPG') # MJPG is encoding supported by Windows
                    # create output video file name
                    # fname_vo = utils.currDate() + "_" + utils.currTime() + "_speeding.avi"
                    fname_vo = "{}_{}_speeding.avi".format(utils.currDate(), utils.currTime())
                    vidParams = (fname_vo, fourcc, utils.frameRate, (frame.shape[1], frame.shape[0]))
                    # configure output video settings
                    out = cv2.VideoWriter(*vidParams)
                    first_video_frame = False
                if utils.message:
                    triggerInfo = {
                        "event": "VehicleSpeed",
                        "speed": realSpeed_mph,
                        "timestamp": utils.currDate() + "--" + utils.currTime(),
                        "speeding": True
                    }
                    if utils.record:
                        triggerInfo['uri'] = "http://gateway" + "/" + fname_vo
                        triggerInfo['offsetframe'] = frameCount
                    utils.trigger(triggerInfo)
                if utils.record and (frameCount - lastStart) < utils.recordLength and not first_video_frame:
                    out.write(frame)
                    print "wrote video frame"
                    frameCount += 1
        # draw the ROI boundary in yellow
        cv2.drawContours(viewFrame, [contour], 0, (0, 255, 255), 1)

        # draw line on the dashes in the rectqngular space
        cv2.line(transformed, tuple(markers_rect[0]), tuple(markers_rect[1]), (255, 0, 0), 2)


        # show road with marked ROI
        cv2.imshow("road", viewFrame)
        # show rectanguler space
        cv2.imshow("transformed", transformed)




        if normer and utils.visual:
            # show region with normalized magnitudes
            cv2.imshow("normalized magnitudes", mag_norm)

        # keyboard interrupts
        k = cv2.waitKey(1) & 0xff

        # if user presses ESC then exit
        if k == 27:
            break

        elif k == ord('r'):
            # run region selection routing
            roi_pts, dash_pts = selectionTools.regionSelectionMode(frame)
            if len(roi_pts) == 4 and len(dash_pts) == 2:
                p00, p01, p11, p10 = roi_pts
                m1, m2 = dash_pts
                M, markers_rect, marker_len, contour = transformTools.transformedParams(p00, p10, p11, p01, m1, m2, q00, q10, q11, q01)

        # save points in current region selection
        elif k == ord('s'):
            pointContainer = {
                "p00" : p00,
                "p01" : p01,
                "p10" : p10,
                "p11" : p11,
                "m1" : m1,
                "m2" : m2
            }
            fname_s = raw_input("Save to file:\t")
            with open(fname_s, 'wb') as handle:
                pickle.dump(pointContainer, handle)
            print "Saved to file:\t{}".format(fname_s)

        # previously new gray frame becomes old one
        prev = nxt

    else:
        if utils.inf:
            cap = cv2.VideoCapture(utils.dest)
        else:
            # if no more frames are returned from video and not on infinite loop end video capture
            break

print "done"

# release video capture and destroy windows
cap.release()

# if video was being recorded, release the video capture
if utils.record and not first_video_frame:
    out.release()

cv2.destroyAllWindows
