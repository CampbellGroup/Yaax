import numpy as np
import h5py
from putilities import*


tempkeys=[]
tempvals = []
dics = ['g1','s2']
vault = ['test.hdf5']
for etr in dics:
    h = ParamVaultut('test.hdf5', etr)
    #print(h.attributecollector())
    keys,vals = h.attributecollector()
    for ktr in keys:
        tempkeys.append(ktr)
    for jtr in vals:
        tempvals.append(jtr)
i = 0 
o = ParamVaultut()
for etr in tempkeys:
    o.write_att('tempvault.hdf5', 'g1', att = etr, val = tempvals[i])
    i+=1 
