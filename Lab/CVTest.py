import numpy as np
import cv2
import time
import CVTest_impl

ci = CVTest_impl.CVTestImpl()

cap = cv2.VideoCapture(0)

ret, frame_first = cap.read()

binary_image = np.ndarray(shape = (frame_first.shape[0:2]), dtype = bool)


cv2.namedWindow('hsv')

cv2.createTrackbar('hMin', 'hsv', 0, 255, ci.do_nothing)  # This is a function handle
cv2.createTrackbar('hMax', 'hsv', 0, 255, ci.do_nothing)
cv2.createTrackbar('sMin', 'hsv', 0, 255, ci.do_nothing)
cv2.createTrackbar('sMax', 'hsv', 0, 255, ci.do_nothing)
cv2.createTrackbar('vMin', 'hsv', 0, 255, ci.do_nothing)
cv2.createTrackbar('vMax', 'hsv', 0, 255, ci.do_nothing)

loop_count = 0
while (True):

    ci.store_frame_time()
    ci.print_fps()

    loop_count += 1
    h_min = cv2.getTrackbarPos('hMin', 'hsv')
    h_max = cv2.getTrackbarPos('hMax', 'hsv')
    s_min = cv2.getTrackbarPos('sMin', 'hsv')
    s_max = cv2.getTrackbarPos('sMax', 'hsv')
    v_min = cv2.getTrackbarPos('vMin', 'hsv')
    v_max = cv2.getTrackbarPos('vMax', 'hsv')

    # Capture frame-by-frame
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hsv_min = np.array([h_min, s_min, v_min], np.uint8)
    hsv_max = np.array([h_max, s_max, v_max], np.uint8)

    hsv_threshed = cv2.inRange(hsv, hsv_min, hsv_max)

    cv2.imshow('binary', hsv_threshed)

    cv2.imshow('hsv', hsv)


    # print loop_count
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()