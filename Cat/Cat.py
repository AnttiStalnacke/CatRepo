import cv2
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
      'When you have it, hold down "r". Hold down "q" to quit.'

# This first while loop is the setup. It sets the threshold values for the squares and for the red dot. After
# completions there should be threshold values for these things.
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
    # cv2.imshow('binary', hsv_opened_closed)

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
        ci.inital_guess_color_squares()
        found_red = True

    # The user presses g if green is found
    if cv2.waitKey(1) == ord('g') and found_red is True:
        hsv_pos_min_squares = hsv_pos_min.copy()
        hsv_pos_max_squares = hsv_pos_max.copy()
        print 'The lower values for the HSV threshold for the green square are', hsv_pos_min_squares
        print 'The upper values for the HSV threshold for the green square are', hsv_pos_max_squares
        found_both = True
# At this point there should be an affine transform to transform the oblique square into a rectangle


# Setup is done. The next wile loop will track the red dot and output it's coordinates. The cat should probably be in
#  this loop as well.

print 'Hold down "q" to quit.'
while True:

    # Press q to quit
    if cv2.waitKey(1) == ord('q'):
        break

    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_threshed = cv2.inRange(hsv, hsv_pos_min_red, hsv_pos_max_red)
    hsv_opened = cv2.morphologyEx(hsv_threshed, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)))
    hsv_opened_closed = cv2.morphologyEx(hsv_opened, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10)))
    # Look for contours and plot those in the original frame
    binary_contours, hierarchy = cv2.findContours(hsv_opened_closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(frame, binary_contours, -1, (0, 255, 0), 3)
    # We only want to look for coords if we actually have a contour
    if hierarchy is not None:
        coord_found, x_coord, y_coord = ci.do_moments_find_coord(binary_contours, hierarchy)
        # x print x_coord, y_coord
        cv2.circle(frame, (x_coord,y_coord),15,180,1)

    cv2.imshow('frame', frame)


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

