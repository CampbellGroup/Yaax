import pandas as pd
import numpy as np 

class DataManager():
    def __init__(self):
        pass

    def collector(self, hold=[], num=int):
        dftemp = pd.read_csv('temp.csv')
        dftemp.iloc[num] = hold
        #print(dftemp) 
        dftemp.to_csv('temp.csv',index=False)

    def setdefault(self,num=int):
        dfdefault = pd.read_csv('defaults.csv')
        a = dfdefault.iloc[num].to_list()[1:]
        return a
    def setparams(self,num=int):
        df = pd.read_csv('temp.csv')
        params = df.iloc[num].to_list()
        return params
if __name__ == '__main__':
    w = DataManager()