from collections import deque
from threading import Lock, Thread
import numpy as np
import time
import myo



class BufferPlus(myo.DeviceListener):
    #An instance of this class constantly collects new EMG data in a queue (buffer)
    def __init__(self, buffer_len):
        self.n = buffer_len
        self.lock = Lock()
        self.mav_data_queue = deque(maxlen=self.n)
            
    # def MAV(self,in_data):
            # #mav_data = []  # 1x8
            # for i in range(0,8):
                # col_data = in_data[:,i]
                # abs_data = np.absolute(col_data)
                # mav_datai = sum(abs_data)/len(abs_data)
                # self.mav_data_queue.append(mav_datai)
            # #mav_data = np.array(mav_data)
            # return self.mav_data_queue

    def get_mav_data(self,in_data):
        mav_data = []
        with self.lock:
            for i in range(0,8):
                col_data = in_data[:,i]
                abs_data = np.absolute(col_data)
                mav_datai = sum(abs_data)/len(abs_data)
                mav_data.append(mav_datai)
            self.mav_data_queue.append(mav_data)
            #self.mav_data_queue = MAV(in_data) 
            return list(self.mav_data_queue)
    
