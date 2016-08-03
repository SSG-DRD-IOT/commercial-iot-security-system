import cv2
import numpy as np

cv2.namedWindow("road")

def setElement(arr, idx, val):
    high_id = len(arr) - 1
    if idx <= high_id:
        arr[idx] = val
    else:
        arr.append(val)
    return arr

def doNothing(event, x, y, flags, param):
    return None

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
        # print "{}: ( {}, {} )".format(param, x, y)

p00, p01, p11, p10, m1, m2 = [None] * 6

def regionSelectionMode():

    global p00, p01, p11, p10, m1, m2, mode, point, max_pt, roi_pt, dash_end, frame, selecting
    frame = np.zeros((360, 640, 3), np.uint8)
    # roi_pt = [(0,0)] * 4
    roi_pt = []
    dash_end = []
    mode = 0 # roi -> 0; dash -> 1
    point = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.setMouseCallback("road", regionSelect, None)
    while(True):
        max_pt = 1 if mode else 3
        modeText = "Dash" if mode else "ROI"
        statString = modeText + (":{}".format(point))
        # print statString


        frame = np.zeros((360, 640, 3), np.uint8)

        cv2.putText(frame, statString, (20,30), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

        for i, pt in enumerate(roi_pt):
            cv2.putText(frame, str(i), pt, font, 1, (255, 0, 0), 1, cv2.LINE_AA)
        for i, pt in enumerate(dash_end):
            cv2.putText(frame, str(i), pt, font, 1, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.imshow("road", frame)

        k = cv2.waitKey(1) & 0xff

        # ENTER
        if k == 13:
            if len(roi_pt)==4 and len(dash_end) == 2:
                p00, p01, p11, p10 = roi_pt
                m1, m2 = dash_end
                print "done selecting"
                break
            elif len(roi_pt) != 4:
                print "switching to position", len(roi_pt)
                point = len(roi_pt)
            elif len(dash_end) != 2:
                print "switching to position", len(dash_end)
                point = len(dash_end)

        # ESC
        elif k == 27:
            print "canceled"
            break
            # if (None in (p00, p01, p11, p10, m1, m2)):
            #     print "Please select all necessary points"
            #     continue
            # else:
            #     print "quitting"
            #     break

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
        # keypress is a number
        elif k in range(ord(str(0)), ord(str(max_pt)) + 1):
            point = k - 48
            print "moving to point", point

        elif k == ord("/"):
            print "killed"
            cv2.destroyAllWindows()
            break
    cv2.setMouseCallback("road", doNothing, None)
regionSelectionMode()
