# Author: XU Tianyu & WANG Xiaoke
# Edit: 2021.3.14
# FM_Final Project: EMG_MAV

# Implement the calculation of MAV (mean absolute value) for all eight channels of the EMG.
# Plot the calculated value on top of the EMG plots.

import myo
import numpy as np
import time
import keyboard
import math

from myo_ecn.listeners                   import ConnectionChecker
from myo_ecn.listeners                   import Buffer
from MultichannelPlot                    import MultichannelPlot
from myo_ecn.listenersPlus               import BufferPlus
#from MAVMultichannelPlot                import MAVMulticChannelPlot             # plot together with 16 channels 
#from MultichannelPlot1                  import MultichannelPlot1
#from features                           import MAV

# def MAV(in_data):
    # mav_data = []  # 1x8
    # for i in range(0,8):
        # col_data = in_data[:,i]
        # abs_data = np.absolute(col_data)
        # mav_datai = sum(abs_data)/len(abs_data)
        # mav_data.append(mav_datai)
    # mav_data = np.array(mav_data)
    # return mav_data


def main():
    # ================== setup myo-python (do not change) =====================
    myo.init(sdk_path='../../myo_sdk') # Compile Python binding to Myo's API
    hub = myo.Hub() # Create a Python instance of MYO API
    if not ConnectionChecker().ok: # Check connection before starting acquisition:
        quit()
    # =========================================================================
    # calculate the Mean Absolute Value
    # Setup our custom processor of MYO's events.
    # EmgBuffer will acquire new data in a buffer (queue):
    listener = Buffer(buffer_len = 512) # At sampling rate of 200Hz, 512 samples correspond to ~2.5 seconds of the most recent data.
    computer = BufferPlus(buffer_len = 15)
    # Setup multichannel plotter for visualisation:
    plotter = MultichannelPlot(nchan = 8, xlen = 15) # Number of EMG channels in MYO armband is 8 , window size is 15 for MAV
  

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
            if (emg_data.ndim==2):
                mav_data = computer.get_mav_data(emg_data)
                mav_data = np.array(mav_data)
           
                
                plotter.update_plot(np.array(mav_data.T))
                
              
            if keyboard.is_pressed('C'):
                print('Stop.')
                break


if __name__ == '__main__':
    main()
