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
            # create the path for bridge IDs
            main_path = os.path.join(arg, str(id))

            # check if the folder already exists and create it if it doesn't
            if os.path.isdir(main_path) == False:
                # create main_path (the folder with ID)
                os.mkdir(main_path)

                for subfolder in subfolders:
                    # create secondary_path (the subfolders inside the main_path)
                    secondary_path = os.path.join(main_path, subfolder)

                    # store the secondary paths only for the 'Previous Reports' subfolder
                    if subfolder == 'Previous Reports':
                        globalvars.folders.append(secondary_path)
                    os.mkdir(secondary_path)

                    # create third_path (the 'old' subfolders of 'Reports' and 'Photos')
                    if subfolder == 'Reports' or subfolder == 'Photos':
                        third_path = os.path.join(secondary_path, 'old')
                        os.mkdir(third_path)

                    elif subfolder == 'Field Notes':
                        third_path = os.path.join(secondary_path, 'Screenshots')
                        os.mkdir(third_path)