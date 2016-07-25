import numpy as np

def showMultiple(img1, img2, img3, img4):
    top = np.concatanate(img1, img2, axis=1)
    bottom = np.concatanate(img3, img4, axis=1)
    total = np.concatanate(top, bottom, axis=0)
    return total
