import numpy as np
import cv2
import time
import CVTest_impl

ci = CVTest_impl.CVTestImpl()

cap = cv2.VideoCapture(0)

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
    hMin = cv2.getTrackbarPos('hMin', 'hsv')
    hMax = cv2.getTrackbarPos('hMax', 'hsv')
    sMin = cv2.getTrackbarPos('sMin', 'hsv')
    sMAx = cv2.getTrackbarPos('sMax', 'hsv')
    vMin = cv2.getTrackbarPos('vMin', 'hsv')
    vMax = cv2.getTrackbarPos('vMax', 'hsv')



    # Capture frame-by-frame
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    cv2.imshow('hsv', hsv)
    # cv2.imshow('hsv2', hsv[:, :, 1])
    # cv2.imshow('hsv3', hsv[:, :, 2])

    cv2.imshow('color', frame)

    # print loop_count
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()