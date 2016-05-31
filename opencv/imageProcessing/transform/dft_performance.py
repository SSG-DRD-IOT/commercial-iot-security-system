"""
Performance of DFT calculation is better when array size = power of 2
arrays whose size is product of 2, 3, and 5 also quite efficient
for performance: ue zero padding
    OpenCV - manually pad 0s
    Numpy - specify new size of FFT calculation, automatically pads 0s
"""
# to calculate optimal size: use OpenCV function: cv2.getOptimalDFTSize()
    # applicable for both cv2.dft() and np.fft.fft2()
cv2.getOptimalDFTSize(rows)
cv2.getOptimalDFTSize(cols)

# pad zeros by creating new big zero array and copy data to it, or use cv2.copyMakeBorder()
nimg = np.zeros((nrows, ncols))
nimg[:rows, :cols] = img

# OR
right = ncols -  cols
bottom = nrows - rows
bordertype = cv2.BORDER_CONSTANT
nimg = cv2.copyMakeBorder(img, 0, bottom, 0, right, bordertype, value = 0)

# openCV functions ~3x faster than Numpy functions 
