"""
Understanding Features

ex. how to put together a puzzle on a computer?
-> look for specific patterns/features that are unique and can easily be tracked and compared

(worst) flat area -> edges -> corners (best)
corners, and in some cases blobs, good features

How to find features / corners?
    look at regions in images with maximum variation when moved in all regions around it
    -> Feature Detection
        once have features and its description, can find same features in all images and
            align
            stitch
            whatever
        to them.
"""
