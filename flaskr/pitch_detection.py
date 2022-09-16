import numpy as np
from scipy.signal import argrelmax
import time


##this file contains various functions
##for calculating main lobe pitch from a block of audio


def getf0(block):
    #max of fourier
    fourier = abs(np.fft.fft(block, n=len(block),axis=0))[:int(len(block)/2)]
    freqs = np.fft.fftfreq(len(fourier), 1/sample_rate)
    pitch = freqs[np.argmax(fourier)]
    return pitch

def zerocrossings(block, fs):
    #count number of times signal changes sign
    zero_crossings = np.nonzero(np.diff(np.sign(block)))[0]
    pitch = len(zero_crossings)/len(block)*fs/2
    return pitch
    
def autocorrelation(prevblock, block, fs):
    #standard autocorrelation implementation
    autoc = np.correlate(np.concatenate((prevblock,block)).ravel(),\
                         prevblock.ravel(),\
                         mode='valid')

    return autoc

def fastautoc(block, fs):
    #fast autocorrelation trick
    fourier = np.fft.fft(block, n=len(block),axis=0).ravel()
    autoc = np.fft.ifft(np.multiply(fourier,np.conjugate(fourier)),n=len(block),axis=0)
    f = findfreq(autoc, fs)
    return f

def findfreq(autoc, fs):
    #find main lobe from autocorrelation block
    maxima = argrelmax(autoc[:int(len(autoc)/2)])
    if not autoc.size:
        return 1
    if not maxima:
        return 1
    if not autoc[maxima].any():
    	return 1
    peak = maxima[0][np.argmax(autoc[maxima])]
    f = (fs/peak)
    return f

def avgdiff(prevblock, block):
    n = len(block)
    twoblock = np.append(prevblock, block)
    diff = np.zeros(n)
    for t in range(n):
        for i in range(n):
            diff[t] += np.square(prevblock[i] - twoblock[i + t])
    return diff


def cmnd(prevblock, block):
    #cumulative mean normalized difference function
    start = time.time()
    n = len(block)
    diff = avgdiff(prevblock, block)
    nordiff = np.zeros(n)
    nordiff[0] = 1
    for t in range(1, n):
        nordiff[t] = np.divide(diff[t], np.sum(nordiff)/t)
    print(time.time() - start)
    return nordiff
    
