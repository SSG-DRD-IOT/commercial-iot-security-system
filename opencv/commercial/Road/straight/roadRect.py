import cv2
import numpy as np
import sympy

def ptAvg(pt1, pt2):
    ptMx = (pt1[0] + pt2[0])/2
    ptMy = (pt1[1] + pt2[1])/2
    ptM = (ptMx, ptMy)
    # return ptM


def regionSelect(event, x, y, flags, param):
    global calcSDAvg, sdList, sdAvg
    if event == cv2.EVENT_LBUTTONDOWN:
        print "{}: ( {}, {} )".format(param, x, y)

cv2.namedWindow("road")
cv2.namedWindow("transformed")

cv2.setMouseCallback("road", regionSelect, "road")
cv2.setMouseCallback("transformed", regionSelect, "rectangle")

marker_len = 10.0 # ft

# {p_ij} --> {q_ij}
frame = cv2.imread("road.jpg")
p00 = (390, 407)
p01 = (464, 407)
p10 = (341, 693)
p11 = (900, 693)

l01 = ptAvg(p00, p01)
l02 = ptAvg(p10, p11)

q00 = (0, 0)
q01 = (250, 0)
q10 = (0, 500)
q11 = (250, 500)

l11 = ptAvg(q00, q01)
l12 = ptAvg(q10, q11)

pts1 = np.float32([p00, p10, p11, p01])
pts2 = np.float32([q00, q10, q11, q01])


cols = max(pts2[:, 0])
rows = max(pts2[:, 1])
M = cv2.getPerspectiveTransform(pts1, pts2)
# print M
# print sympy.Matrix(M).rref()

v1i = np.array((472, 466))
v1f = np.array((467, 458))
v2i = np.array((500, 503))
v2f = np.array((488, 489))
v3i = np.array((548, 574))
v3f = np.array((528, 541))

a1i = (472, 466)
a1f = (467, 458)
a2i = (500, 503)
a2f = (488, 489)
a3i = (548, 574)
a3f = (528, 541)

# cv2.arrowedLine(frame, tuple(v1i), tuple(v1f), (0, 255, 0), 2)
# cv2.arrowedLine(frame, tuple(v2i), tuple(v2f), (0, 255, 0), 2)
# cv2.arrowedLine(frame, tuple(v3i), tuple(v3f), (0, 255, 0), 2)

# vecs = np.array([v1i, v1f, v2i, v2f, v3i, v3f])
vecs = np.array([[v1i, v1f, v2i, v2f, v3i, v3f]], dtype = np.float32)
# print vecs
# print type(vecs)

# u = cv2.perspectiveTransform(vecs, M)
u = cv2.perspectiveTransform(vecs, M)
u = u[0] # u contains an extra layer of depth that needs to be removed
# u = cv2.perspectiveTransform(np.array([[551, 576]]), M)

# print "u is {}".format(u)
transformed = cv2.warpPerspective(frame, M, (cols, rows))
# print "size of transformed is: {}".format(np.shape(transformed))
cv2.arrowedLine(transformed, tuple(u[0]), tuple(u[1]), (0, 255, 0), 2)
cv2.arrowedLine(transformed, tuple(u[2]), tuple(u[3]), (0, 255, 0), 2)
cv2.arrowedLine(transformed, tuple(u[4]), tuple(u[5]), (0, 255, 0), 2)

pts = np.int32(pts1)
pts = pts.reshape((-1, 1, 2))
pts = np.array(pts)
# print pts, type(pts)
cv2.polylines(frame, [pts], True, (0, 255, 255))
cv2.line(frame, l01, l02, (0, 0, 255), 2)
cv2.imshow("road", frame)
cv2.line(transformed, l11, l12, (0, 0, 255), 2)
cv2.imshow("transformed", transformed)


cv2.waitKey(0)
cv2.destroyAllWindows()
