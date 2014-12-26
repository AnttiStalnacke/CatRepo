import numpy as np
import cv2
import time



class CVTestImpl():

    def __init__(self):
        self.time_vec = np.zeros((5))
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

    def do_nothing(self):
        pass

    def print_fps(self):
        print self.fps