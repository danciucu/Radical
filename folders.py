import os
import globalvars



class create():
    def __init__(self, arg):
        
        # import global variables
        globalvars.init()

        # create folders and subfolders
        subfolders = ['Check Prints', 'Field Notes', 'Photos', 'Previous Reports', 'Report']
        subsubfolders = ['Screenshots', 'old']
        main_path = ''
        secondary_path = ''
        third_path = ''

        for id in globalvars.bridgeID:
            main_path = os.path.join(arg, str(id))
            os.mkdir(main_path)
            for subfolder in subfolders:
                secondary_path = os.path.join(main_path, subfolder)  
                if subfolder == 'Previous Reports':
                    globalvars.folders.append(secondary_path)
                os.mkdir(secondary_path)

                if subfolder == 'Reports' or subfolder == 'Photos':
                    third_path = os.path.join(secondary_path, 'old')
                    os.mkdir(third_path)
                elif subfolder == 'Field Notes':
                    third_path = os.path.join(secondary_path, 'Screenshots')
                    os.mkdir(third_path)