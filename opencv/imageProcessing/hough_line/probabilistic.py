"""
Probabilistic Hough Transform

    in HT, even for line w/ 2 arguments, lots of computation
Probabilistic Hough Transform is optimization of HT we saw
    only considers random subset of points
        sufficient for line detection
    have to decrease threshold
function: cv2.HoughLinesP()
    2 arguments:
    minLineLength - min length of line; segments shorter than this rejected
    maxLineGap = max allowed gap between line segments to treat them as single line
