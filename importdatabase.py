import globalvars
import pandas as pd



class bridgeID():
    def __init__(self, arg):

        # import global variables
        globalvars.init()

        bridge_database = pd.read_excel(arg)
        globalvars.bridgeID = bridge_database['Bridge ID'].dropna()