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
    fps = ci.get_fps()
    print fps

    # Get positions of the trackbars
    hsv_pos_min, hsv_pos_max = ci.get_all_trackbar_pos() #TODO
    # hsv_pos_min = np.array([0, 0, 0])
    # hsv_pos_max = np.array([90, 128, 128])

    # Get a frame
    ret, frame = cap.read()

    # Convert it to HSV to simplify thresholding
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold
    hsv_threshed = cv2.inRange(hsv, hsv_pos_min, hsv_pos_max)

    # Open and close to remove artifacts
    hsv_opened = cv2.morphologyEx(hsv_threshed, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10)))
    hsv_opened_closed = cv2.morphologyEx(hsv_opened, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10)))
    hsv_opened_closed_contour = hsv_opened_closed.copy()

    # Look for contours and plot those in the orignal frame
    binary_contours, hierarchy = cv2.findContours(hsv_opened_closed_contour, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(frame, binary_contours, -1, (0, 255, 0), 3)

    # We only want to look for coords if we actually have a contour
    if hierarchy is not None:
        coord_found, x_coord, y_coord = ci.do_moments_find_coord(binary_contours, hierarchy)

        # Abd we inly print the coords if we actually found some
        if coord_found is True:
            print 'X:', x_coord, 'Y:', y_coord



    # Show the opened and closed image
    cv2.imshow('binary', hsv_opened_closed)

    # Show the original hsv image
    cv2.imshow('frame', frame)

    # Count loop for future use
    loop_count += 1

    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()