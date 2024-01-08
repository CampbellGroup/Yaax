import numpy as np
import h5py



hdf = h5py.File("D:/Yaax/testcode/parametervault_v1.hdf5", "r")

base_items = list(hdf.items())
    
print("items in base directory: ",base_items)

x = hdf.get('Urukul')
dds = list(x.items())

print("DDS: ", dds)

aomdp_369 = x.get('/Urukul/u0/c0')

keys = list(aomdp_369.attrs.keys())
vals = list(aomdp_369.attrs.values())

print(keys, "\n",vals)  

hdf.close()
