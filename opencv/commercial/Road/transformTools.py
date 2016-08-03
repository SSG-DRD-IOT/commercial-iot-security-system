import numpy as np
import cv2

# get perspective transformation from spaces P -> Q
def getPerspective(p00, p10, p11, p01, q00, q10, q11, q01):
    # float array of corners in original ROI
    pts1 = np.float32([p00, p10, p11, p01])
    # float array of corners in perspective transform
    pts2 = np.float32([q00, q10, q11, q01])
    # generate perspective transform matrix from ROI
    M = cv2.getPerspectiveTransform(pts1, pts2)
    return M

# get and apply persp transform on merker points
def transformedParams(p00, p10, p11, p01, m1, m2, q00, q10, q11, q01):
    M = getPerspective(p00, p10, p11, p01, q00, q10, q11, q01)
    contour = np.array([p00, p01, p11, p10], dtype = np.int32).reshape((-1, 1, 2))
    # form dash endpoints into an array
    markers = np.float32([[m1, m2]])
    # perform perspective transform on dash marker points
    markers_rect = cv2.perspectiveTransform(markers, M)
    # remove extra layer put on markers by transform
    markers_rect = markers_rect[0]
    # find length of markers in rectangular space
    marker_len = np.linalg.norm(markers_rect[0] - markers_rect[1])
    return M, markers_rect, marker_len, contour
