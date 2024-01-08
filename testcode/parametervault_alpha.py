import numpy as np
import h5py

#Open and construct the parameter vault :

matrix1 = np.array([200,0.38,0])
matrix2 = np.array([200,0.3,0])
null = np.array([0,0,0])

#creat and open the file
hdf = h5py.File("D:/Yaax/testcode/parametervault_v1.hdf5", "w")

#Create DDS Group

#Urukul 0
u0c0 = hdf.create_group('Urukul/u0/c0')
u0c1 = hdf.create_group('Urukul/u0/c1')
u0c2 = hdf.create_group('Urukul/u0/c2')
u0c3 = hdf.create_group('Urukul/u0/c3')

#Urukul 1
u1c0 = hdf.create_group('Urukul/u1/c0')
u1c1 = hdf.create_group('Urukul/u1/c1')
u1c2 = hdf.create_group('Urukul/u1/c2')
u1c3 = hdf.create_group('Urukul/u1/c3')

#Urukul 2
u2c0 = hdf.create_group('Urukul/u2/c0')
u2c1 = hdf.create_group('Urukul/u2/c1')
u2c2 = hdf.create_group('Urukul/u2/c2')
u2c3 = hdf.create_group('Urukul/u2/c3')

#set attributes
u0c0.attrs['freq'] = 200
u0c0.attrs['amp'] = 0.38
u0c0.attrs['attenuation'] = 0.0

u0c1.attrs['freq'] = 200
u0c1.attrs['amp'] = 0.2
u0c1.attrs['attenuation'] = 0.0

u1c0.attrs['freq'] = 200
u1c0.attrs['amp'] = 0.3
u1c0.attrs['attenuation'] = 0.0

hdf.close()