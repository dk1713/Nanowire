# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 16:54:11 2019

@author: dk1713
"""

import os
import numpy as np
import pickle
import nwObjects
os.system("clear")

# L = 20:       0 -> 2
# L = 100:      0 -> 10
W = 5
L = 100
minPeriod = 0
maxPeriod = 4.
periodBs = np.arange(minPeriod,maxPeriod+.5,.5)
M = 0.07

print("\nGenerating Nanowire Data (periodB = %2.1f --> %2.1f)..." 
      %(minPeriod,maxPeriod))

for i in range(np.size(periodBs)):
    ## Set up Nanowire Object ##
    nanowire = nwObjects.Nanowire(width=W, length=L, periodB=periodBs[i], M=M)
    data = nanowire.spectrum(bValues=np.linspace(0, .5, 101))
    
    
    ## Spectrum ##
    pickle.dump(data,
                open("spec" 
                     + "%i.%i.%2.1f.%1.2f" %(W, L, periodBs[i], M)
                     + ".dat", "wb"))
    
print("\nCompleted!")