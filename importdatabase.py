import globalvars
import pandas as pd



class bridgeID():
    def __init__(self, arg):

        # import global variables
        globalvars.init()

        try:
            bridge_database = pd.read_excel(arg)
            globalvars.bridgeID = bridge_database['Bridge ID'].dropna()
            globalvars.error_message = ''
        except:
            globalvars.error_message = "Error: Bridge Database Was Not Imported!"