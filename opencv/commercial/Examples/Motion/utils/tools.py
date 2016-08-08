import numpy as np

def distMap(frame1, frame2):
    """outputs pythagorean distance between two frames"""
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
    dist = np.uint8(norm32*255)
    return dist

def applyNoise(frame, scale):
    noises_p = np.random.rand(*np.shape(frame))
    noises_n = -np.random.rand(*np.shape(frame))
    noises = (noises_p + noises_n) * 255 * scale
    noiseFrame = frame + np.uint8(noises)
    return noiseFrame
