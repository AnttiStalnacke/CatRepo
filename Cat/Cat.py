import numpy as np
import cv2
import time
import Cat_impl

# Create instance of CVTestImpl
ci = Cat_impl.CatImpl()

# Start capturing video
cap = cv2.VideoCapture(0)

# Setup thresholds to find red dot
found_red = False
found_both = False
# Open a new windows
cv2.namedWindow('trackbars')
# This image is only used to make the trackbars a bit bigger, ugly
img = cv2.imread('white.jpeg')
cv2.imshow('trackbars', img)
# Create all the trackbars
ci.create_all_trackbars()
ci.inital_guess_red_dot()

print 'Pull on the trackbars so that only the red dot is visible in the binary image.\n' \
      'When you have it press "r". Press "q" to quit.'

while found_both is False:

    # Get positions of the trackbars
    hsv_pos_min, hsv_pos_max = ci.get_all_trackbar_pos()

    # Get a frame
    ret, frame = cap.read()

    # Convert it to HSV to simplify thresholding
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold
    hsv_threshed = cv2.inRange(hsv, hsv_pos_min, hsv_pos_max)

    # Open and close to remove artifacts
    hsv_opened = cv2.morphologyEx(hsv_threshed, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)))
    hsv_opened_closed = cv2.morphologyEx(hsv_opened, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10)))

    # Show the opened and closed image
    cv2.imshow('binary', hsv_opened_closed)

    # Show the original hsv image
    cv2.imshow('frame', frame)

    # Show the threshed image
    cv2.imshow('threshed', hsv_threshed)

    # Press q to quit
    if cv2.waitKey(1) == ord('q'):
        break

    # The user presses r if red is found
    if cv2.waitKey(1) == ord('r') and found_red is False:
        hsv_pos_min_red = hsv_pos_min.copy()
        hsv_pos_max_red = hsv_pos_max.copy()
        print 'The lower values for the HSV threshold for the red dot are', hsv_pos_min_red
        print 'The upper values for the HSV threshold for the red dot are', hsv_pos_max_red
        print 'Now find the black squares and press "g" when done'
        ci.inital_guess_green_square()
        found_red = True

    # The user presses b if black is found
    if cv2.waitKey(1) == ord('g') and found_red is True:
        hsv_pos_min_black = hsv_pos_min.copy()
        hsv_pos_max_black = hsv_pos_max.copy()
        print 'The lower values for the HSV threshold for the green square are', hsv_pos_min_black
        print 'The upper values for the HSV threshold for the green square are', hsv_pos_max_black
        found_both = True


# Setup thresholds to find black squares


    # Main while loop
    # Find squares
    # Affine
    # Find dot


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

