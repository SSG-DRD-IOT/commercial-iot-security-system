import cv2
import numpy as np

# sets array to value at index or appends to array if index doesn't exist
def setElement(arr, idx, val):
    high_id = len(arr) - 1
    if idx <= high_id:
        arr[idx] = val
    else:
        arr.append(val)
    return arr

# callback function for selecting a region
def regionSelect(event, x, y, flags, param):
    global mode, point, max_pt, roi_pt, dash_end
    max_pt = 1 if mode else 3
    if event == cv2.EVENT_LBUTTONDOWN:
        if mode:
            if point <= max_pt:
                dash_end = setElement(dash_end, point, (x, y))
                point += 1
            else:
                print "Press ENTER to save new points or ESC to cancel"
        else:
            if point <= max_pt:
                roi_pt = setElement(roi_pt, point, (x, y))
                point += 1
                if point > max_pt:
                    mode = not mode
                    point = 0

# subroutine that runs to select the ROI
def regionSelectionMode(frame):
    global mode, point, max_pt, roi_pt, dash_end, selecting
    roi_pt = []
    dash_end = []
    mode = 0 # roi -> 0; dash -> 1
    point = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.namedWindow("Selection")
    cv2.setMouseCallback("Selection", regionSelect, None)
    while(True):
        showFrame = np.copy(frame)
        max_pt = 1 if mode else 3
        modeText = "Dash" if mode else "ROI"
        statString = modeText + (":{}".format(point))

        cv2.putText(showFrame, statString, (20,30), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

        for i, pt in enumerate(roi_pt):
            cv2.putText(showFrame, str(i), pt, font, 1, (255, 0, 0), 1, cv2.LINE_AA)
        for i, pt in enumerate(dash_end):
            cv2.putText(showFrame, str(i), pt, font, 1, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.imshow("Selection", showFrame)

        k = cv2.waitKey(1) & 0xff


        if k == 13: # ENTER
            if len(roi_pt)==4 and len(dash_end) == 2:
                print "done selecting"
                break
        elif k == 27: # ESC
            print "canceled"
            roi_pt = []
            dash_end = []
            break
        elif k == ord('e'):
            if point < max_pt:
                print "moving to next point"
                point += 1
            elif not mode:
                print "moving to dash"
                mode = 1
                point = 0
        elif k == ord('q'):
            if point > 0:
                print "moving to previous point"
                point -= 1
            elif mode:
                print "moving to roi"
                mode = 0
                point = 4
        elif k in range(ord(str(0)), ord(str(max_pt)) + 1): # keypress is a number
            point = k - 48
            print "moving to point", point
    cv2.destroyWindow("Selection")
    return roi_pt, dash_end
