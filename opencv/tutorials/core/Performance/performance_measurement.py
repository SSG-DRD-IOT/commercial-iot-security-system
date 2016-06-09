"""
performance measurement and improvement techniques
- meaure code performance
- tips to improve performance of code
functions:
cv2.
    getTickCount()
    getTickFrequency()
python provides modules:
- "time" for meauring execution time
- "profile" for detailed report on the code
- features integrated into iPython
"""

# Measuring performance with OpenCV
# cv2.getTickCount returns # of clock cycles after a reference event (like moment machine switched on)
#   to moment function is called; call it before and after fun execution
# cv2.getTickFrequency returns freq of clock cycles or # of cycles per second

# find time of execution in seconds
e1 = cv2.getTickCount()
# your code execution
e2 = cv2.getTickCount()
time = (e2 - e1)/ cv2.getTickFrequency()

# example: apply median filtering with a kernel of odd size ranging from 5 to 49
img1 = cv2.imread('messi5.jpg')

e1 = cv2.getTickCount()
for i in xrange(5, 49, 2):
    img1 = cv2.medianBlur(img1, i)
e2 = cv2.getTickCount()
t = (e2 - e1)/cv2.getTickFrequency()
print t

# result is 0.5211 seconds

# NOTE: can do the same with "time" module; use time.time() instead of cv2.getTickCount


# Default Optimization in OpenCV

# many functions optimized using SSE2, AVX, ...
# OpenCV runs optimized code if it's enabled, otherwise unoptimized code
# use cv2.useOptimized() to check if enabled/disabled, cv2.setUseOptimized to enable/disable it

# check if optimization is enabled
cv2.useOptimized()

%timeit res = cv2.medianBlur(img, 49)

# disable it
cv2.setUseOptimized(False)
cv2.useOptimized()

%timeit res = cv2.medianBlur(img, 49)
# optimized median filtering 2x faster than unoptimized version
# median filtering is SIMD optimized


# Measuring Performance in Python

# sometimes, need to compare performance of 2 similar operations
# ipython has magic command timeit
# python scalar operations are faster than Numpy scalar operations
# for operations incl 1 or 2 elements, Python scalar better than numpy arrays
#   numpy advantage when size of array is bigger

# compare performance of cv2.countNonZero() and np.count_nonzero()
%timeit z = cv2.countNonZero(img) # 25x faster than Numpy function
%timeit z = np.count_nonzero(img)


# Performance Optimization Techniques

# NOTE: first implement algorithm in simple manner; once working, profile it, find the bottlenecks, and optimize them
#   1. avoid using loops in Python as far as possible, esp. double/triple loops (they're inherently slow)
#   2. vectorize the algorithm/code to the max poss extent b/c Numpy and OpenCV are optimized for vector operations
#   3. exploit the cache coherence
#   4. never make copies of arrays unless needed. Try to use views instead. Array copying is a costly operation.
# If code is still slow, use add'l libs like Cython to make faster
