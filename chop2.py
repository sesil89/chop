# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 15:17:47 2016

@author: robacha
"""

from __future__ import division
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

#get zvec and correct for negative values
zvec = np.genfromtxt('2013_09_12__14_12_06h_zvec.csv', delimiter=',')*(-1)

signal = np.genfromtxt('2013_09_12__14_12_06h_ImageJ.txt', delimiter='\t')

ratio = len(signal)/len(zvec)

zvec_diff = np.diff(zvec)

zvec_thresholded = zvec_diff < -100

#plt.plot(zvec_thresholded)

#zvec_thresholded2 = zvec_thresholded > 100

positions = np.nonzero(zvec_thresholded)

newpositions = np.ndarray.round(positions[0] * ratio).astype(int)



print positions, newpositions, ratio

# this a comment

# now resample

zvec_resampled = scipy.signal.resample(zvec, len(signal)-1)

#plt.plot(zvec_resampled)
#plt.plot(zvec)

# cut out individual runs

ncuts = len(newpositions)-1
thematrix = np.zeros(shape=(26000,50))

roiid = int(raw_input("Which ROI would you like to analyse?\n>>> "))
sign = []

for a in range(0, ncuts):
    
    if a == 0:
        z = zvec_resampled[1:newpositions[a]]
        data = signal[1:newpositions[a],:]
        p = np.round(z*100).astype(int)
               
        test = scipy.signal.resample(data,25000,p)
        mytest = test[0]
#        plt.plot(mytest[:,roiid])
    
        sign.append((mytest[:,roiid]))
        
    else:
        z = zvec_resampled[newpositions[a]:newpositions[a+1]]
        data = signal[newpositions[a]:newpositions[a+1],:]
        p = np.round(z*100).astype(int)
              
        test = scipy.signal.resample(data,25000,p)
        mytest = test[0]
#        plt.plot(mytest[:,roiid])
    
        sign.append((mytest[:,roiid]))
        

i=0
for array in sign:
    
    plt.subplot(len(sign)+1, 1, i+1)
    plt.plot(sign[i])
    i+=1
    
plt.subplot(len(sign)+1, 1, i+1)
plt.imshow(sign, aspect="auto")
#
#
#thematrix[p,:] = data
#plt.plot(z)

#fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=(6,10))

