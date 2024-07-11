import numpy as np
import h5py

#Open and construct the parameter vault :

matrix1 = np.array([200,0.38,0])
matrix2 = np.array([200,0.3,0])
null = np.array([0,0,0])

#creat and open the file
with h5py.File("D:/Yaax/testcode/attributetests.hdf5", "r") as hdf:

    base_items = list(hdf.items())
    print("items in base directory: ",base_items)
    x = hdf.get('g1/s1')

    t = x.attrs.get('test')

    #print(x)


