# -*- coding: utf-8 -*-
"""
Created on Wed Mar 02 10:31:10 2016

@author: robacha
"""

from __future__ import division
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
import glob
import os


def ratio(zvec, signal):
    """Calculates the ratio between the number of zvec and signal samples."""
    
    ratio = len(signal)/len(zvec)
    return ratio
    

def get_positions(zvec, ratio):
    """Gets the cutting positions from thresholding the max. values of changes in zvec
    and multiplying it by the ratio (to fit the resampled values)."""
    
    zvec_diff = np.diff(zvec)
    zvec_thresholded = zvec_diff < -100
    positions = np.nonzero(zvec_thresholded)
    newpositions = np.ndarray.round(positions[0] * ratio).astype(int)
    return newpositions
    #print positions, newpositions
    
    
def resample(zvec, signal):
    """resamples zvec values to fit the number of signal samples."""
    
    zvec_resampled = scipy.signal.resample(zvec, len(signal))
    return zvec_resampled
    

    
def chop(zvec_resampled, signal, newpositions):
    """Cuts the zvec and sample data into pieces fitting one round of the corridor run."""  
    
    ncuts = len(newpositions)-1      
    sign = []

    for cut in range(0, ncuts):
        
        if cut == 0:
            zvec_cut = zvec_resampled[0:newpositions[cut]]
            signal_cut = signal[0:newpositions[cut],:]
            p = np.round(zvec_cut*100).astype(int)
            
            signal_resampled = scipy.signal.resample(signal_cut,25000,p)
            mytest = signal_resampled[0]
    #        plt.plot(mytest[:,roiid])
        
            sign.append(mytest[:,roiid])
            
        else:
            zvec_cut = zvec_resampled[newpositions[cut]:newpositions[cut+1]]
            signal_cut = signal[newpositions[cut]:newpositions[cut+1],:]
            p = np.round(zvec_cut*100).astype(int)
            
            signal_resampled = scipy.signal.resample(signal_cut,25000,p)
            mytest = signal_resampled[0]
    #        plt.plot(mytest[:,roiid])
        
            sign.append(mytest[:,roiid])
            
    return sign
    
#def plot (sign):
#    """Plots the signal values and a heatmap from one ROI for all the runs"""
#    
#    i=0
#    for array in sign:
#        plt.subplot(len(sign)+1, 1, i+1)
#        plt.plot(sign[i])
#        i+=1
#    
#    plt.subplot(len(sign)+1, 1, i+1)
#    plt.imshow(sign, aspect="auto")
#
#

if __name__ == "__main__":
    #pathname = 'C:/Users/robacha/Desktop/chop'
        
    file_list_signal =  glob.glob(os.getcwd() + '/*.txt')
    
    file_list_zvec2 = glob.glob(os.getcwd() + '/*.csv')
    
    file_list_zvec = []
    
    #do smth to make it universal
    for filename in file_list_zvec2:
        if  filename[0:51] in [f[0:51] for f in file_list_signal]:
            file_list_zvec.append(filename)
            
    
    #get all signal and zvec files into arrays and correct for negative values when necessary
    zvec_array = []
    
    signal_array = []
    
    for file_path in file_list_zvec:
        zvec_array.append(np.genfromtxt(file_path, delimiter=',')*(-1))
    
    
    #how to skip the first column???
    for file_path in file_list_signal:
        signal_array.append(np.genfromtxt(file_path, delimiter='\t', skip_header = 1))
        
        
        
    roiid = int(raw_input("Which ROI would you like to analyse?\n>>> "))
    
    ratio_array = []
    for a, b in zip(signal_array, zvec_array):
        #or b in zvec_array:
            ratio_array.append(ratio(b, a))
            
    positions_array = []
    for b, ratio in zip(zvec_array, ratio_array):
        #for ratio in ratio_array:
            positions_array.append(get_positions(b, ratio))
            
    zvec_resampled_array = []  
    for a, b in zip(signal_array, zvec_array):
        #for b in zvec_array:
            zvec_resampled_array.append(resample(b, a))
    
    
    chopped_array= []
    for zvec, signal, positions in zip(zvec_resampled_array, signal_array, positions_array):
        chopped_array.append(chop(zvec, signal, positions))
        
    #plot(sign)
    
    
    
    #sign = []
    #
    #i=0
    #for array in sign:
    #    plt.subplot(len(sign)+1, 1, i+1)
    #    plt.plot(sign[i])
    #    i+=1
    #    
    #plt.subplot(len(sign)+1, 1, i+1) 
    #plt.imshow(sign, aspect="auto")
    
    
    
    
    
    
    ##thematrix = np.zeros(shape=(26000,50))
    #
    #thematrix[p,:] = data
    #plt.plot(z)
    
    #fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=(6,10))
    
