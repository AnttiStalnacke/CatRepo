import numpy as np
import cv2
import time


class CatImpl():

    def __init__(self):
        self.time_vec = np.zeros((5))
        self.hsv_pos_min = np.zeros(3, dtype=int)
        self.hsv_pos_max = np.zeros(3, dtype=int)
        self.time_new = 0
        self.time_old = 0
        self.fps = 0

    def get_fps(self):

        self.time_old = self.time_new
        self.time_new = time.time()
        time_of_frame = self.time_new - self.time_old
        self.time_vec[1:4] = self.time_vec[0:3]
        self.time_vec[0] = time_of_frame
        self.fps = 1/self.time_vec.mean()
        return self.fps

    def _do_nothing(self, remove_type_error):
        pass

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

    def inital_guess_red_dot(self):
        cv2.setTrackbarPos('hMin', 'trackbars', 0)
        cv2.setTrackbarPos('hMax', 'trackbars', 180)
        cv2.setTrackbarPos('sMin', 'trackbars', 0)
        cv2.setTrackbarPos('sMax', 'trackbars', 255)
        cv2.setTrackbarPos('vMin', 'trackbars', 198)
        cv2.setTrackbarPos('vMax', 'trackbars', 255)

    def inital_guess_color_squares(self):
        cv2.setTrackbarPos('hMin', 'trackbars', 57)
        cv2.setTrackbarPos('hMax', 'trackbars', 94)
        cv2.setTrackbarPos('sMin', 'trackbars', 56)
        cv2.setTrackbarPos('sMax', 'trackbars', 196)
        cv2.setTrackbarPos('vMin', 'trackbars', 54)
        cv2.setTrackbarPos('vMax', 'trackbars', 229)

    def do_moments_find_coord(self, binary_contours, hierarchy):

        max_area = 0
        coord_found = False
        num_of_objects = hierarchy.shape[1]
        # And we only want to do things if we have actually filtered out a few contours
        if num_of_objects < 4:
            # print 'num_of_objects:', num_of_objects
            for i in range(0, num_of_objects):

                moments = cv2.moments(binary_contours[i])

                # If the area is smaller than 400 pixels it's likely noise
                if moments['m00'] > 4: #TODO Not true in future
                    if moments['m00'] > max_area:
                        max_area = moments['m00']

                        x_coord = int(moments['m10']/moments['m00'])
                        y_coord = int(moments['m01']/moments['m00'])
                        coord_found = True

        if coord_found is True:
            return coord_found, x_coord, y_coord
        else:
            # An error seems to occur if the number of returned variables change
            return coord_found, 0, 0

