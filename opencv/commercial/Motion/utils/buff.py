def genBuffMask(bufferFrames):
    'create bitwise mask for buffer length'
    buffMask = 1
    for i in range(0, bufferFrames-1):
        buffMask = (buffMask)<<1 | buffMask
    return buffMask
