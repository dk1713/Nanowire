#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 23:30:48 2019

@author: Domi
"""
import os
import numpy as np
import pickle
import nwObjects
os.system("clear")

W = 5
minN = 3
maxN = 15
Ns = np.arange(minN,maxN+1,2)
M = 0.05
added = False

print("\nGenerating Nanowire Data (noSections = %i --> %i) and added: %r..." 
      %(minN,maxN, added))

for i in range(np.size(Ns)):
    ## Set up Nanowire Object ##
    nanowire = nwObjects.Nanowire(width=W, noSections=Ns[i], M=M, addedSinu=added)
    
    ## Spectrum ##
    pickle.dump(nanowire.spectrum(bValues=np.linspace(0, 1, 201)),
                open("data/spec" 
                     + "w%i.no%i.m%1.2f.added%i" %(W, Ns[i], M, int(added))
                     + ".dat", "wb"))

    ## Conductance ##
    pickle.dump(nanowire.conductances(bValues=np.linspace(0, 1, 201)),
                open("data/cond" 
                     + "w%i.no%i.m%1.2f.added%i" %(W, Ns[i], M, int(added))
                     + ".dat", "wb"))
    
print("\nCompleted!")