import numpy as np
import cv2

class Track:
    
    # Initialize with initial parameters for ROI
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        
    def getInitialFrame(self, file = 0, image = False):
        
        # Gives the option to initialize on a still image, which can using the algorithm easier
        if image == True:
            frame = cv2.imread(file)
        else:
            # initialize video from the webcam
            # If a file is selected, it will populate here
            # otherwise 0 is default, which is a live feed from a webcam
            video = cv2.VideoCapture(file)
        
            # Read the videp
            cap, frame = video.read()

            # if the capture isn't successful, return None
            if not cap:
                return None
        
        # set up region of interest (roi)
        roi = frame[self.y:self.y + self.height, self.x:self.x + self.width]
        
         # apply mask
        hsv_frame =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_frame, np.array((0, 20, 20)), np.array((180, 250, 250)))
        hist_frame = cv2.calcHist([hsv_frame], [0], mask, [180], [0,180])
        cv2.normalize(hist_frame, hist_frame, 0, 255, cv2.NORM_MINMAX)
        
        if not image:
            # Turn off the camera
            video.release()
        
        return hist_frame
    
    def objectTrack(self, hist_frame, shift = "cam"):
        
        # Initialize the track window
        track_window = (self.x, self.y, self.width, self.height)
        
        # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
        
        # Initialize camera
        video = cv2.VideoCapture(0)
        
        while True:

            # Read video
            ret, frame = video.read()

            if ret == True:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                dst = cv2.calcBackProject([hsv],[0],hist_frame,[0,180],1)

                # apply whichever mean/cam shift
                if shift == "cam":
                    ret, track_window = cv2.CamShift(dst, track_window, term_crit)
                    
                    # Draw it on image
                    pts = cv2.boxPoints(ret)
                    pts = np.int0(pts)
                    img2 = cv2.polylines(frame,[pts],True, 255,2)
                    cv2.imshow('img2',img2)

                elif shift == "mean":
                    ret, track_window = cv2.meanShift(dst, track_window, term_crit)
                   
                    # Draw static rectangle on image
                    img2 = cv2.rectangle(frame, (self.x, self.y), (self.x + self.width, self.y + self.height), 255,2)
                    cv2.imshow('img2',img2)
                    
                else:
                    print("Use a valid method. This function only permits 'mean' for mean shift and 'cam' for cam shift.")
                    break


                # Use the q button to quit the operation
                if cv2.waitKey(60) & 0xff == ord('q'):
                    break

            else:
                break

        cv2.destroyAllWindows()
        video.release()