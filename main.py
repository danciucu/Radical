import tkinter, ttkthemes, tkinter.filedialog
import globalvars, folders, importdatabase, downloadfiles
import os



class Radical(ttkthemes.ThemedTk):
    def __init__(self):
        super().__init__()

        # import global variables
        globalvars.init()

        # configure the root window
        self.title('Radical')
        self.geometry('450x360')
        #self.iconphoto(False, tkinter.PhotoImage(file = "logo1.png"))
        self.set_theme('radiance')

        # define a frame
        self.main_frame = tkinter.ttk.Frame(self)
        self.main_frame.pack()
        ## label for username
        self.username_label = tkinter.ttk.Label(self.main_frame, text = 'Username')
        self.username_label.grid(row = 0, column = 1)
        ## entry for username
        self.username_entry = tkinter.ttk.Entry(self.main_frame, width = 30, state = tkinter.NORMAL)
        self.username_entry.grid(row = 2, column = 1)
        ## label for password
        self.password_label = tkinter.ttk.Label(self.main_frame, text = 'Password')
        self.password_label.grid(row = 3, column = 1)
        ## entry for password
        self.password_entry = tkinter.ttk.Entry(self.main_frame, width = 30, state = tkinter.NORMAL)
        self.password_entry.grid(row = 4, column = 1)
        ## label for importing data
        self.import_label = tkinter.ttk.Label(self.main_frame, text = 'Import an Excel file with bridge ID')
        self.import_label.grid(row = 6, column = 1)
        ## entry for importing data
        self.import_entry = tkinter.ttk.Entry(self.main_frame, width = 40, state = tkinter.NORMAL)
        self.import_entry.grid(row = 7, column = 1)
        ## button for importing data
        self.import_button = tkinter.ttk.Button(self.main_frame, text = '...', state = tkinter.NORMAL, command = self.excel_import, width = 2)
        self.import_button.grid(row = 7, column = 2) 
        ## label for save folder
        self.save_label = tkinter.ttk.Label(self.main_frame, text = 'Select the folder where files will be downloaded')
        self.save_label.grid(row = 8, column = 1)
        ## entry for save folder
        self.save_entry = tkinter.ttk.Entry(self.main_frame, width = 40, state = tkinter.NORMAL)
        self.save_entry.grid(row = 9, column = 1)
        ## button for save folder
        self.save_button = tkinter.ttk.Button(self.main_frame, text = '...', state = tkinter.NORMAL, command = self.folder_path, width = 2)
        self.save_button.grid(row = 9, column = 2) 
        ## Photo Document checkbox
        self.var1 = tkinter.IntVar()
        self.cbox1 = tkinter.ttk.Checkbutton(self.main_frame, text = 'Photo Document', variable = self.var1, onvalue = 1, offvalue = 0)
        self.cbox1.grid(row = 10, column = 1)
        ## Plans checkbox
        self.var2 = tkinter.IntVar()
        self.cbox2 = tkinter.ttk.Checkbutton(self.main_frame, text = 'Plans', variable = self.var2, onvalue = 1, offvalue = 0)
        self.cbox2.grid(row = 11, column = 1)
        ## Report Document checkbox
        self.var3 = tkinter.IntVar()
        self.cbox3 = tkinter.ttk.Checkbutton(self.main_frame, text = 'Report Document', variable = self.var3, onvalue = 1, offvalue = 0)
        self.cbox3.grid(row = 12, column = 1)
        ## Previous Report Document checkbox
        self.var4 = tkinter.IntVar()
        self.cbox3 = tkinter.ttk.Checkbutton(self.main_frame, text = 'Previous Report', variable = self.var4, onvalue = 1, offvalue = 0)
        self.cbox3.grid(row = 13, column = 1)
        ## button for starting the process
        self.save_button = tkinter.ttk.Button(self.main_frame, text = 'Start', command = self.download_files, state = tkinter.NORMAL, width = 4)
        self.save_button.grid(row = 14, column = 1) 


    # define function that imports the Excel file:
    def excel_import(self):
        # variable that handles the Excel path
        path = tkinter.filedialog.askopenfilename(filetypes = (
            ("Excel Files", "*.XLSX"),
            ("All Files", "*.*")
        ))
        # fill entry bar with the path
        self.import_entry.insert(tkinter.END, path)
        # import bridge IDs
        importdatabase.bridgeID(path)

    # define function that imports the Excel file:
    def folder_path(self):
        # variable that handles the Excel path
        folder_path = tkinter.filedialog.askdirectory()
        # update user_var
        count = 0
        i = 0
        j = 0
        for k in range(len(folder_path)):
            if folder_path[k] == "/":
                count += 1
            elif count == 2 and i == 0:
                i = k
            elif count == 3:
                j = k - 1
                break
        globalvars.user_path = folder_path[i:j]
        # fill entry bar with the path
        self.save_entry.insert(tkinter.END, folder_path)
        # check if the folder selected is empty
        if not os.listdir(folder_path):
            print("empty")
            # create folders and subfolders
            folders.create(folder_path)
        else:
            print("not empty")

            
        

    # define function that downalods files from NBIS website
    def download_files(self):
        # update username and password
        globalvars.username = self.username_entry.get()
        globalvars.password = self.password_entry.get()
        # update the checkboxes
        globalvars.cb1var = self.var1.get()
        globalvars.cb2var = self.var2.get()
        globalvars.cb3var = self.var3.get()
        globalvars.cb4var = self.var4.get()
        print(globalvars.cb1var)
        print(globalvars.cb2var)
        print(globalvars.cb3var)
        # download files
        downloadfiles.previous_reports()


if __name__ == "__main__":
    app = Radical()
    app.mainloop()