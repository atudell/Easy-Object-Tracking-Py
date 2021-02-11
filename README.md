# Easy-Object-Tracking-Py

Easy Object Tracking is a python script to help make mean shift and cam shift object tracking easier to implement. It also serves as a demonstration of skill and practice with Python and OpenCV.

Easy Object Tracking is written in an object oriented manner. 

Initialization: x and y are the coordinates of the initial Region of Interest (ROI) and the width and height are the dimensions of the tracking window.

example = Track(x = 0, y = 0, width = 100, height = 100)

Initial Frame: By default, the script will automatically take the current frame from a web cam (if it's available). A pre-recorded video may be used instead by passing
its address to the file parameter. Instead of a video, an image may also be used by passing its address to the file parameter and passing the image parameter as true.
This can potentially simplify the process by passing an image of the object that needs to be tracked.
Note that this method returns a histogram that will be used to pass through the tracking method.

hist = example.getInitialFrame(file = 0, image = False)

Tracking: The objectTrack method takes the histogram from the previous method so that it can use histogram back projection to find the object. The shift parameter may be "mean"
for the mean shift algorithm or "cam" for the cam shift algorithm. Any other value will result in an error. By default, cam shift is used. Once implemented, the camera will turn
on and begin to track the specified object based on color. The program may be terminated by pressing "q".

example.objectTrack(hist_frame = hist, shift = "cam")
