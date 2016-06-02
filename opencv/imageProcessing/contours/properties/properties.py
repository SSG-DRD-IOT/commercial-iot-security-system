"""
extract useful info like Solidity, equivalent diameter, mask image, mean intensity, ...
See Matlab regionprops docs for more features
(centroid, area, perimeter also belong to this cat)
"""

# Aspect ratio
# ratio of width to height of bounding rect of object
# Aspect Ratio = Width / Height
x, y, w, h = cv2.boundingRect(cnt)
aspect_ratio = float(w)/h

# Extent
# ratio of contour area to bounding rect area
# Extent = Object Area / Bounding Rect Area
area = cv2.contourArea(cnt)
x, y, w, h = cv2.boundingRect(cnt)
rect_area = w*h
extent = float(area) / rect_area

# Solidity
# ratio of contour area to its convex hull area
# Solidity = contour area / convex hull area
area = cv2.contourArea(cnt)
hull = cv2.convexHull(cnt)
hull_area = cv2.contourArea(hull)
solidity = float(area)/hull_area

# Equivalent Diameter
# diameter of the circle whose area is same as contour area
# Equivalent Diameter = sqrt(4 * contour area / pi)
area = cv2.contourArea(cnt)
equi_diameter = np.sqrt(4*area / np.pi)

# Orientation
# angle at which object is directed
(x,y), (MA, ma), angle = cv2.fitEllipse(cnt)

# Mask and Pixel pts
# may need all the pts which comprise object
mask = np.zeros(imgray.shape, np.uint8)
cv2.drawContours(mask, [cnt], 0, 255, -1)
pixelpoints = np.transpose(np.nonzero(mask))
# pixelpoints = cv2.findNonZero(mask)
# both Numpy and OpenCV functions do the same
# numpy in (row, col) format, OpenCV in (x, y) format (answers interchanged)
# NOTE: row=x, col=y

# Max, Min vals and their locations
# find parameters using mask image
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(imgray, mask = mask)

# Mean color or Mean Intensity
# find avg color of an object
# or avg intensity of object in grayscale mode; uses same mask
mean_val = cv2.mean(im, mask = mask)

# Extreme Points
# topmost, bottommost, rightmost and leftmost points of the object
leftmost = tuple(cnt[:,:,0].argmin()][0])
rightmost = tuple(cnt[:,:,0].argmax()][0])
topmost = tuple(cnt[:,:,1].argmin()][0])
bottommost = tuple(cnt[:,:,1].argmax()][0])
