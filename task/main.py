
# This script is a estima1tor for Moving Mean Average Value
import matplotlib.pyplot as plt
import myo
import numpy as np
import time
import keyboard

from myo_ecn.listeners                   import ConnectionChecker
from myo_ecn.listeners                   import Buffer
from MultichannelPlot                    import MultichannelPlot 

def main():
    # ================== setup myo-python (do not change) =====================
    myo.init(sdk_path='../../myo_sdk') # Compile Python binding to Myo's API
    hub = myo.Hub() # Create a Python instance of MYO API
    if not ConnectionChecker().ok: # Check connection before starting acquisition:
        quit()
    # =========================================================================


    # Setup our custom processor of MYO's events.
    # EmgBuffer will acquire new data in a buffer (queue):
    listener = Buffer(buffer_len = 512) # At sampling rate of 200Hz, 512 samples correspond to ~2.5 seconds of the most recent data.

    # Setup multichannel plotter for visualisation:
    plotter = MultichannelPlot(nchan = 8, xlen = 512) # Number of EMG channels in MYO armband is 8
    #plotter2 = MultichannelPlot(nchan = 8, xlen = 512) 
    N1 = 0
    q = 0
    j = 0
    # Tell MYO API to start a parallel thread that will collect the data and
    # command the MYO to start sending EMG data.
    with hub.run_in_background(listener): # This is the way to associate our listener with the MYO API.
        print('Streaming EMG ... Press shift-c to stop.')
        while hub.running:
            time.sleep(0.040)
            # Pull recent EMG data from the buffer
            emg_data = listener.get_emg_data()
            # Transform it to numpy matrix
            emg_data = np.array([x[1] for x in emg_data])
            
            # q = q+1
            # if q >= 100: 
                # q = 0
                # N = 0
                # for i in range(1,len(emg_data)):
                    # N[j] = N[j] + emg_data[i]                
                # N1[j] = N[j]/(len(emg_data))
                # j = j+1
                # print('\rRecording ... %d percent done.' % N[j], end='\n')  
                
                
            # Plot it
            plotter.update_plot(emg_data.T)
            
            # Plot Moving Mean Average Value
            
            #plotter2.update_plot(N1,j)
            plt.plot(N1,j, color="r", linestyle="-", linewidth=1)
            plt.show()
   
            
            if keyboard.is_pressed('C'):
                print('Stop.')
                break


if __name__ == '__main__':
    main()
    
def mav(emg_data):
    c
    if q >= 100: 
    q = 0
    N = 0
    for i in range(1,len(emg_data)):
        N[j] = N[j] + emg_data[i]                
    N1[j] = N[j]/(len(emg_data))
    j = j+1
    print('\rRecording ... %d percent done.' % N[j], end='\n')  
    
    
    


# ---------------------
class Moving_Average(object):
    def __init__(self, length, return_int = False):
        self.data = []
        self.data_sum = -1
        #self.data_avg = -1
        self.length = length
        self.value = -1
        self.return_int = return_int

        #self.sample_frequency = sample_frequency               #in Hz
        #self.range_ = range_                                   #in seconds
        #self.scope = 1.0 * self.sample_frequency * self.range_       #in number of samples, limits the length of movingAvg    
        #self.sum_movingAvg = 0                                 #tracks the sum of the moving average
        #self.val_movingAvg = -1                                #the latest moving average value
        #self.movingAvg = []                                    #used to store the datapoints for taking a moving average

    def get_movingAvg (self, data):
        self.data.insert(0, data)
        self.data_sum += data

        if len(self.data) > self.length:
            self.data_sum -= self.data.pop()

        if self.return_int == True:
            self.value = int(self.data_sum / self.length) #preserves integer form
        else: 
            self.value = 1.0 * self.data_sum / self.length

        if len(self.data) < (self.length / 2):
            return -1
        else:
            return self.value