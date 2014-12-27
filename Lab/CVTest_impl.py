import numpy as np
import cv2
import time



class CVTestImpl():

    def __init__(self):
        self.time_vec = np.zeros((5))
        self.hsv_pos_min = np.zeros(3, dtype=int)
        self.hsv_pos_max = np.zeros(3, dtype=int)
        self.time_new = 0
        self.time_old = 0
        self.fps = 0

    def store_frame_time(self):

        self.time_old = self.time_new
        self.time_new = time.time()
        time_of_frame = self.time_new - self.time_old
        self.time_vec[1:4] = self.time_vec[0:3]
        self.time_vec[0] = time_of_frame
        self.fps = 1/self.time_vec.mean()

    def _do_nothing(self):
        pass

    def print_fps(self):
        print self.fps

    def create_all_trackbars(self):

        cv2.createTrackbar('hMin', 'trackbars', 0, 180, self._do_nothing)  # This is a function handle
        cv2.createTrackbar('hMax', 'trackbars', 0, 180, self._do_nothing)
        cv2.createTrackbar('sMin', 'trackbars', 0, 255, self._do_nothing)
        cv2.createTrackbar('sMax', 'trackbars', 0, 255, self._do_nothing)
        cv2.createTrackbar('vMin', 'trackbars', 0, 255, self._do_nothing)
        cv2.createTrackbar('vMax', 'trackbars', 0, 255, self._do_nothing)

    def get_all_trackbar_pos(self):

        self.hsv_pos_min[0] = cv2.getTrackbarPos('hMin', 'trackbars')
        self.hsv_pos_max[0] = cv2.getTrackbarPos('hMax', 'trackbars')
        self.hsv_pos_min[1] = cv2.getTrackbarPos('sMin', 'trackbars')
        self.hsv_pos_max[1] = cv2.getTrackbarPos('sMax', 'trackbars')
        self.hsv_pos_min[2] = cv2.getTrackbarPos('vMin', 'trackbars')
        self.hsv_pos_max[2] = cv2.getTrackbarPos('vMax', 'trackbars')

        return self.hsv_pos_min, self.hsv_pos_max