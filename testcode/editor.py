import numpy as np
import h5py

class Editor():
    def __init__(self):
        pass
    #THIS FILES TAKES IN CREATES NEW GROUPS AND EDITS ATTRIBUTES:
    def write_att(self, path, loc, att=None, val=None):

        with h5py.File(path, 'a') as hdf:

            if hdf.get(loc) != None:
                if val == None or att == None:
                    pass
                else:
                    g = hdf.get(loc)
                    g.attrs.modify(att,val)
            else :  
                if val == None or att == None:
                    g = hdf.create_group(loc)
                else:
                    g = hdf.create_group(loc)
                    g.attrs.modify(att,val)

    #GENERAL ATTRIBUTE READER: 
    def read_att(self, path, loc, att):
        with h5py.File(path, 'r') as hdf:
            g = hdf.get(loc)
            v = g.attrs.get(att)
            print(v)

    #THIS WILL DISPLAY ALL OF THE GROUPS AND SUBGROUPS:
    def display(self, path):
        with h5py.File(path, 'r') as hdf:
            h = []
            def displayer(name):
                #print(name)
                h.append(name)
                print(h)

            hdf.visit(displayer)
        return h
    
    #PATH CHECKER:
    def pathchecker(self,path):
        hdf = h5py.File(path, 'a')

        if hdf.get('meta') != None:
            g = hdf.create_group('meta')
        
        else: 
            pass

        hdf.close()