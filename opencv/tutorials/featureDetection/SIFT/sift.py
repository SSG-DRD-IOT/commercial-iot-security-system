"""
Intro to SIFT (Scale-Invariant Feature Transform)

concepts of SIFT algorithm
SIFT keypoints and descriptors

Corner detectors (eg Harris) - rotation-invariant
    even if image rotated, can find same corners
        bc corners remain corners in a rotated image
but SCALING - corner may not be a corner if image is scaled
    corner in small image wi small window is flat when zoomed in same window
    -> Harris corner is not scale invariant

SIFT - extracts keypoints and computes descriptors
    see: Distinctive Image Features from Scale-Invariant Keypoints by D. Lowe
4 steps involved
    1. scale-space extrema detection
        we can't use same window to detect keypoints with different scale
            OK with small corner
        to detect larger corners, need larger windows
            scale-space filtering is used
        Laplacian of Gaussian is found for image with various \sigma values
        LoG - acts as blob detector; detects blobs of various sizes due to change in \sigma
            \sigma is scaling parameter
                gaussian kernel with low \sigm gives hi val for small corner
                    ... with high \sigma fits well for larger corner
                can find local maxima across scale and space, giving a list of (x, y, \sigma) vals
                    potential keypt at (x, y) at \sigma scale
        BUT LoG costly, so SIFT uses Difference of Gaussians
            DoG is approximation of LoG
        DoG obtained as difference of Gaussian blurring of image w/ 2 different \sigma
            let it be \sigma, k * \sigma
        process done for different octaves of image in Gaussian Pyramid
        once DoG found, images searched for local extrema over scale and space
            eg. one pixel in an image is compared w/ 8 neighbors as well as 9 pixels in next scale and 9 pixels in previous scales
        paper empirical data:
            # of octaves = 4
              of scale levels = 5
            initial \sigma = 1.6
            k = sqrt(2)
            ^ optimal values
