"""
Contours Hierarchy (notes)

in cv2.findContours(), pass argument Contour Retrieval Mode
    usually pass cv2.RETR_LIST or cv2.RETR_TREE
output, have 3 arrays: 1) image, 2) contours, 3) hierarchy

use cv2.findContours to detect objects in image
    some are in different locations
    some are nested inside one-another
        call outer one "parent", inner "child"
can specify how one contour connected to others
    i.e. if it is a child or a parent
represent relationship with a "hierarchy"

external or outermost contours: hierarchy-0 or "in the same hierarchy level"
contour of inner box is hierarchy-1
terms: same hierarchy level, external contour, child contour, parent contour, first child

Hierarchy Representation in openCV

each contour has own info wrt what hierarchy it is, who's its child, parent, etc.
array of 4 values:
    [Next, Previous, First_Child, Parent]
        (Next denotes next contour @ same hierarchical level)
ex. if contour-0, next contour @ same lvl is contour-1, for contour-1 it's contour-2 so Next = 2
    contour-2 has no next contour @ same lvl, so Next=-1
Previous denotes previous contour @ same hierarchical lvl
(if no previous, put -1)
First_Child denotes first child contour
Parent denotes index of its parent contour
No child or parent -> field is -1

Contour Retrieval Modes in OpenCV:
flags like
cv2.
    RETR_LIST,  RETR_TREE, RETR_CCOMP, RETR_EXTERNAL
"""
# RETR_LIST:
    # simplest
    # retrieves all contours, but doesn't create any parent-child relationship
    # PARENTS & KIDS ARE EQUAL; are just contours--belong to same hierarchy level
        # 3rd, 4th term in hierarchy array always -1; Next, Previous terms have corresponding values
# ex. from before
print hierarchy

# RETR_EXTERNAL
    # returns only extreme outer flags
        # all child contours left behind
    # only eldest in each family is taken care of
print hierarchy

# RETR_CCOMP
    # retrieves all contours, arranges in a 2-lvl hierarchy
        # ie external contours of object (boundary) are placed in hierarchy 1, contours of holes inside object placed in hierarchy 2
    # essentially, outer circles belong to 1st hierarchy, inner circles in 2nd

# RETR_TREE
    # retrieves all contours, creates full family hierarchy list
    # tells who everybody is
