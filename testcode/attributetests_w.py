import numpy as np
import h5py

#Open and construct the parameter vault :

matrix1 = np.array([200,0.38,0])
matrix2 = np.array([200,0.3,0])
null = np.array([0,0,0])

#creat and open the file
hdf = h5py.File("D:/Yaax/testcode/attributetests.hdf5", "w")

g11 = hdf.create_group('g1/s1')

g11.attrs.modify('test',123)

hdf.close()

