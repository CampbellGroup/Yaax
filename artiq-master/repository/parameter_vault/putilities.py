import numpy as np
import h5py


class ParamVaultut():
    def __init__(self, path = None, expname= None):
        
        if path == None or expname == None: 
            print("No path and/or group selected!")
        
        else:
            self.path = path
            with h5py.File(self.path, 'r') as hdf:
                def set_group(name):
                    if expname in name:
                        return name
                self.loc = hdf.visit(set_group)
        
            #print(self.path, self.loc)

    #WRITE AN ATTRIBUTE 
    def write_att(self, path= None, loc = None, att=None, val=None):

        if path == None :
            path = self.path
        if loc == None :
            loc = self.loc 

        with h5py.File(path ,'a') as hdf:

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
    def read_att(self, att, path = None, loc = None):

        if path == None :
            path = self.path 
        if loc == None :
            loc = self.loc

        with h5py.File(path, 'r') as hdf:
            g = hdf.get(loc)
            v = g.attrs.get(att)
            print(v)

    #THIS WILL DISPLAY ALL OF THE GROUPS AND SUBGROUPS:
    def display(self, path= None):

        if path == None :
            path = self.path 

        with h5py.File(path, 'r') as hdf:
            h = []
            def displayer(name):
                #print(name)
                h.append(name)
                print(h)

            hdf.visit(displayer)
        return h
    
    #PATH CHECKER:
    def pathchecker(self,path = None):

        if path == None :
            path = self.path 

        hdf = h5py.File(path, 'a')

        if hdf.get('meta') == None:
            g = hdf.create_group('meta')
        
        else: 
            pass

        hdf.close()

    #Attribute Collector: 
    def attributecollector(self, path = None, loc= None):

        if path == None :
            path = self.path 
        if loc == None :
            loc = self.loc

        with h5py.File(path,'a') as hdf:
            g = hdf.get(loc)
            keys = list(g.attrs.keys())
            values = list(g.attrs.values())

        return keys,values