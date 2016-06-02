"""
Fourier Transform

-Find Fourier Transform of images using OpenCV
-utilize FFT functions in Numpy
-FT applications

functions:
cv2.
    dft()
    idft()

FT used to analyze freq characteristics of filters
for images
    2D Discrete Fourier Transform used to find frequency domain
FFT calculates DFT
sinusoidal signal: x(t)=A * sin(2 * \pi *f * t)
    f - freq signal
        if freq domain taken, can see a spike at f
    if signal sampled to form discrete signal, get same freq domain, but periodic in range:
        [- \pi , \pi] or [0, 2 * \pi] (or [0, N] for N-pt DFT)
consider image a signal sampled in 2 directions
    taking FT in both X and Y dirs gives freq representation of image
for sinusoidal signal, if ampl varies fast in time -> hi freq signal
for images:
    amplitude varies drastically at edge points or noises
    therefore edges and noises high freq contents of image
    no changes in amplitude: lo freq component
"""
# FT in Numpy
    # numpy has FFT package
    # np.fft.fft2 prov. freq transform which is complex array
    # arguments:
        # input image (grayscale)
        # size of output array; if greater than size of input image, input image padded w/ 0s before calculation of FFT
            # less than input image: input image cropped
            # no args passes: output size same as input
    # result: zero freq component @ top left corner
        # to bring to center: shift result by N/2 in both directions
            # done by np.fft.fftshift()
    # once find frequency transform -> find magnitude spectrum

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('messi5.jpg', 0)
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
magnitude_spectrum = 20*np.log(np.abs(fshift))

plt.subplot(121), plt.imshow(img, cmap='gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()

# can see whiter region at center, showing low freq content is prominent
# ^ found freq transform; now, can do ops in freq domain
    # hi pass filtering
    # image reconstruction (ie find inverse DFT)
        # remove lo freqs with rectangular window, size 60x60
        # apply inverse shift using np.fft.ifftshift()
            # so DC component is again at top right hand corner
        # find inverse FFT using np.ifft2()
            # result complex #; take its abs value
rows, cols = img.shape
crow, ccol = rows/2, cols/2
fshift[crow-30:crow+30, ccol-30:ccol+30] = 0
f_ishift = np.fft.ifftshift(fshift)
img_back = np.fft.ifft2(f_ishift)
img_back = np.abs(img_back)

plt.subplot(131),plt.imshow(img, cmap = 'gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(132),plt.imshow(img_back, cmap = 'gray')
plt.title('Image after HPF'), plt.xticks([]), plt.yticks([])
plt.subplot(133),plt.imshow(img_back)
plt.title('Result in JET'), plt.xticks([]), plt.yticks([])

plt.show()

# don't use rectangular filters for masking
    # create ripple-like ringing effects
    # mask converted to sinc shape, causing problem
        # use Gaussian window instead

# Fourier Transform in OpenCV
# functions: cv2.dft() and cv2.idft()
    # same result as before, but in 2 channels
        # 1st channel: real part of result
        # 2nd channel: imaginary part
# convert input image to np.float32 first

import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('messi5.jpg', 0)

dft = cv2.dft(np.float32(img), flags = cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)

magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:,:,0], dft_shift[:,:,1]))

plt.ubplot(121), plt.imshow(img, cmap = 'gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()
# NOTE: use cv2.cartToPolar(), which returns both magnitude and phase

# now, we do inverse DFT
# previously, we created HPF
# now, remove hi freq contents of image
# -> apply LPF
    # blurs the image

# create a mask first with high value, 1, @ low freq
    # ie pass LF content
# 0 at HF region
rows, cols = img.shape
crow, ccol = rows/2, cols/2

# create mask first, center square is 1, all remaining zeros
mask = np.zeros((rows, cols, 2), np.uint8)
mask[crow-30:crow+30, ccol-30:ccol+30] = 1

# apply mask and iDFT
fshift = dft_shift * mask
f_ishift = np.fft.ifftshift(fshift)
img_back = cv2.idft(f_ishift)
img_back = cv2.magnitude(img_back[:,:,0], img_back[:,:,1])

plt.subplot(121), plt.imshow(img, cmap = 'gray)
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(img_back, cmap = 'gray)
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()
