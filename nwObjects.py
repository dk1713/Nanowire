#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 01:42:41 2019

@author: Domi
"""

import kwant
import tinyarray as ta
import numpy as np
import scipy.sparse.linalg

from tqdm import trange

s_0 = np.identity(2)
s_z = np.array([[1., 0.], [0., -1.]])
s_x = np.array([[0., 1.], [1., 0.]])
s_y = np.array([[0., -1j], [1j, 0.]])

tau_z = ta.array(np.kron(s_z, s_0))
tau_x = ta.array(np.kron(s_x, s_0))
tau_y = ta.array(np.kron(s_y, s_0))
sig_z = ta.array(np.kron(s_0, s_z))
sig_x = ta.array(np.kron(s_0, s_x))
sig_y = ta.array(np.kron(s_0, s_y))
tau_zsig_x = ta.array(np.kron(s_z, s_x))
tau_zsig_y = ta.array(np.kron(s_z, s_y))

## Functions ##
def makeNISIN(W=5, L=20, barrierLen=1, periodB=.5, isWhole=True):
    def onsiteSc(site, t, B, Delta):
        if periodB == 0:
            return (4 * t) * tau_z + B * sig_x + Delta * tau_x
        else:
            theta = 2*np.pi*periodB*(site.pos[0] - barrierLen)/(L - 1 - 2*barrierLen)
            return (4 * t) * tau_z + B * (sig_x*np.cos(theta) - sig_y*np.sin(theta)) + Delta * tau_x
    def onsiteNormal(site, mu, t):
        return (4 * t - mu) * tau_z
    def onsiteBarrier(site, mu, t, barrier):
        return (4 * t - mu + barrier) * tau_z
    def hop(site0, site1, t, alpha):
        return -t * tau_z - .5j * alpha * tau_zsig_y
    
    # On each site, electron and hole orbitals.
    lat = kwant.lattice.square(norbs=4) 
    syst = kwant.Builder()
    
    # S
    syst[(lat(i, j) for i in range(1,L-1) for j in range(W))] = onsiteSc
    
    if isWhole:
        # I's
        syst[(lat(i, j) for i in range(barrierLen) for j in range(W))] = onsiteBarrier
        syst[(lat(i, j) for i in range(L-barrierLen, L)for j in range(W))] = onsiteBarrier
        syst[lat.neighbors()] = hop
    
        # N's
        lead = kwant.Builder(kwant.TranslationalSymmetry((-1,0)),
                             conservation_law=-tau_z
                             )
        lead[(lat(0, j) for j in range(W))] = onsiteNormal
        lead[lat.neighbors()] = hop
    
        syst.attach_lead(lead)
        syst.attach_lead(lead.reversed())
    else:
        syst[lat.neighbors()] = hop

    return syst.finalized()

## Objects ##
class Nanowire:
    def __init__(self, width, length, barrierLen, periodB):
        self.width = width
        self.length = length
        self.barrierLen = barrierLen
        self.periodB = periodB
        
    def spectrum(self, bValues=np.linspace(0, 1.0, 101)):
        syst = makeNISIN(W=self.width, L=self.length, 
                         barrierLen=self.barrierLen, 
                         periodB=self.periodB, 
                         isWhole=False)
        
        energies = []
        params = dict(
                mu=.3, Delta=.1, alpha=.8, t=1.0, barrier = .5
                )
        for i in trange(np.size(bValues)):
            params["B"] = bValues[i]
            H = syst.hamiltonian_submatrix(sparse=True,  params=params)
            H = H.tocsc()
            eigs = scipy.sparse.linalg.eigsh(H, k=20, sigma=0)
            energies.append(np.sort(eigs[0]))
            
        # Returns dict
        outcome = dict(B=bValues, E=energies)
        return outcome
    
    def conductances(self, 
                     bValues=np.linspace(0, 0.35, 36),
                     energies=[0.001 * i for i in range(-140, 140)]
                     ):
        syst = makeNISIN(W=self.width, L=self.length, 
                         barrierLen=self.barrierLen, 
                         periodB=self.periodB, 
                         isWhole=True)
        
        data = []
        params = dict(
                mu=.3, Delta=.1, alpha=.8, t=1.0, barrier = .5
                )
        for i in trange(np.size(energies)):
            cond = []
            energy = energies[i]
            for b in bValues:
                params["B"] = b
                smatrix = kwant.smatrix(syst, energy, params=params)
                cond.append(smatrix.transmission((1, 1), (0, 0)))
            data.append(cond)
        
        outcome = dict(B=bValues, BiasV=energies, Cond=data)
        return outcome

def main():
    pass

if __name__ == '__main__':
    main()