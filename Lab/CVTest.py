import numpy as np
import cv2
import time
import CVTest_impl

# Create instance of CVTestImpl
ci = CVTest_impl.CVTestImpl()

# Start capturing video
cap = cv2.VideoCapture(0)

# Open a new windows
cv2.namedWindow('trackbars')
# This image is only used to make the trackbars a bit bigger, ugly
img = cv2.imread('white.jpeg')
cv2.imshow('trackbars', img)

# Create all the trackbars
ci.create_all_trackbars()

loop_count = 0
while (True):

    # Just used to count FPS
    ci.store_frame_time()
    ci.print_fps()

    # Get positions of the trackbars
    hsv_pos_min, hsv_pos_max = ci.get_all_trackbar_pos()

    # Get a frame
    ret, frame = cap.read()

    # Convert it to HSV to simplify thresholding
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold
    hsv_threshed = cv2.inRange(hsv, hsv_pos_min, hsv_pos_max)

    # Open and close to remove artifacts
    hsv_opened = cv2.morphologyEx(hsv_threshed, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))
    hsv_opened_closed = cv2.morphologyEx(hsv_opened, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))

    # Show the opened and closed image
    cv2.imshow('binary', hsv_opened_closed)

    # Show the original hsv image
    cv2.imshow('hsv', hsv)

    # Count loop for future use
    loop_count += 1

    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()