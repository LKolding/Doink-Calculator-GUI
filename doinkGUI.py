from tkinter import *
from tkinter.messagebox import showinfo
from tkinter import ttk
from listboxscroll import ScrollBox

import dbHandler

MARGIN = 10
DB_FILE_PATH = "db.json"
SETTINGS_FILE_PATH = "settings.json"

class GUI_template(Toplevel):
    def __init__(self, title: str):
        Toplevel.__init__(self)
        self.title(title)
        self.resizable(FALSE, FALSE)
        self.createWidgets()
    
    def createWidgets(self): '''both creates and grids widgets'''
    def gridWidgets(self): '''DEPRECIATED, YET STILL IN USE, GL UNDERSTANDING THIS'''

# Main menu window
class MainGUI(GUI_template):
    
    def __init__(self, master: Tk):
        self.frame = Frame(master)
        self.frame.pack()
        
        self.createWidgets()
    
    def createWidgets(self):
        self.topframe = Frame(self.frame)
        self.botframe = Frame(self.frame)

        self.title_label = Label(self.topframe, text="Doinkydoinky")
        self.title_label.config(font=("Futura", 36))

        self.view_db_button = Button(self.botframe,text="View DB", command=self.viewDBWindow)
        self.add_person_button = Button(self.botframe,text="Add person",  command=self.addPersonWindow)
        self.add_doink_button = Button(self.botframe,text="Add doink",  command=self.addDoinkWindow)
        self.clear_person_button = Button(self.botframe,text="Clear person",  command=self.clearPersonWindow)
        self.separator = ttk.Separator(self.botframe,orient='horizontal')
        self.settings_button = Button(self.botframe,text="Settings",  command=self.settingsWindow)
        self.quit_button = Button(self.botframe,text="Quit",  command=exit)
        self.gridWidgets()

    def gridWidgets(self):
        self.title_label.grid()

        # row 1
        self.view_db_button.grid(row=0,column=0)
        self.add_person_button.grid(row=0,column=1)
        # 2
        self.add_doink_button.grid(row=1,column=0)
        self.clear_person_button.grid(row=1,column=1)
        # 3
        self.separator.grid(row=2,columnspan=2,sticky="EW", pady=(18,14))
        # 4
        self.settings_button.grid(row=3,column=0)
        self.quit_button.grid(row=3,column=1)

        EXTRA_MARGIN = 15
        self.topframe.grid(row=0, padx=MARGIN+EXTRA_MARGIN,pady=MARGIN+EXTRA_MARGIN)
        self.botframe.grid(row=1, padx=MARGIN+EXTRA_MARGIN,pady=MARGIN+EXTRA_MARGIN)

    def viewDBWindow(self): ViewDB("Database")
    def addPersonWindow(self): AddPerson("Add person")
    def addDoinkWindow(self): AddDoink("Add Doink")
    def clearPersonWindow(self): ClearPerson("Clear person")
    def settingsWindow(self): Settings("Settings")

# Add doink dialog
class AddDoink(GUI_template):
    def __init__(self, title):
        self.handler = dbHandler.Handler(DB_FILE_PATH)
        GUI_template.__init__(self, title)
    
    def createWidgets(self):
        self.midframe = Frame(self)
        self.botframe = Frame(self)
        # middle
        self.weed_label = Label(self.midframe, text="weed")
        self.weed_entry = Entry(self.midframe)
        self.smokes_label = Label(self.midframe, text="smokes")
        self.smokes_entry = Entry(self.midframe)
        self.incl_date = Checkbutton(self.midframe, text="Include date")
        
        # LIST OF USERS
        self.users_list = Listbox(self.botframe, height=4)
        users = self.handler.getUsers()
        
        # IF NO USERS, SHOW ERROR
        if not users: self.users_list.insert(1,"NO USERS")
        
        for no,user in enumerate(users): self.users_list.insert(no,user)
    
        # bottom
        self.add_doink_button = Button(self.botframe, text="Add", command=self.submit)
        self.gridWidgets()
        
    def gridWidgets(self):
        self.weed_label.pack(side="left")
        self.weed_entry.pack(side="left")
        self.smokes_label.pack(side="left")
        self.smokes_entry.pack(side="left")
        self.incl_date.pack(side="left")
        self.incl_date.select() #defaults adding date to entry
        self.users_list.pack()
        self.add_doink_button.pack()
        
        self.midframe.pack(padx=MARGIN,pady=MARGIN)
        self.botframe.pack(padx=MARGIN,pady=MARGIN)

    def submit(self):
        weed: float
        smokes: float
        try:
            weed = float(self.weed_entry.get())
            smokes = float(self.smokes_entry.get())
        except:
            showinfo(title='Error', message=f"Please enter weed and smokes amount as decimal point numbers")
            return
        
        user: str
        try:
            user = self.users_list.get(self.users_list.curselection())
            if user == "NO USERS": raise ValueError
            
        except ValueError:
            showinfo(title='Error', message=f'add a proper user ya dingkus')
            self.destroy()
        
        except: showinfo(title='Error', message=f"Please select a user")
        
        else:
            # store doink info in database file
            try: self.handler.saveDoink(user, smokes, weed)
            except: showinfo(title="Error", message=f"Couldn't store doink in database. Consider to verify if all values are correct and file 'db.json' isn't corrupted or protected.")
            else:
                showinfo(title="Success", message=f"Doink has been saved in {user}'s ledger")
                self.destroy()
            
# Add person dialog
class AddPerson(GUI_template):
    def __init__(self, title):
        self.handler = dbHandler.Handler(DB_FILE_PATH)
        GUI_template.__init__(self,title)
    
    def createWidgets(self):
        self.name_entry = Entry(self, text="name")
        self.add_person_button = Button(self, text="Add", command=self.submit)
        self.gridWidgets()
        
    def gridWidgets(self):
        self.name_entry.pack(padx=MARGIN,pady=MARGIN)
        self.add_person_button.pack(padx=MARGIN,pady=MARGIN)
        
    def submit(self):
        try: 
            name: str = self.name_entry.get()
            if name == "": 
                showinfo(title="Oh no tewi", message="I'm gonna need an actual name")
                return
            
            self.handler.addPerson(str(self.name_entry.get()))
            
        except: showinfo(title="This is horrible", message="something went wrong and i wont spend time to figure it out")
        else: 
            showinfo(title="Success",message=f"{name} has been added!")
            self.destroy()

# Clear person dialog
class ClearPerson(GUI_template):
    
    def __init__(self,title):
        self.handler = dbHandler.Handler(DB_FILE_PATH)
        GUI_template.__init__(self,title)
    
    def createWidgets(self):
        self.usersVariable = StringVar()
        self.users_cbBox = ttk.Combobox(self, textvariable=self.usersVariable)
        
        self.choose_user_label = Label(self, text="Choose user...")
        
        self.users_cbBox['values'] = self.handler.getUsers() # gets list of all users from db
        self.users_cbBox['state'] = "readonly"
        
        self.clear_person_button = Button(self, text="Clear", command=self.submit)
        self.gridWidgets()
        
    def gridWidgets(self):
        self.choose_user_label.pack(pady=MARGIN, padx=MARGIN)
        self.users_cbBox.pack(padx=MARGIN,pady=MARGIN)
        self.clear_person_button.pack(padx=MARGIN,pady=MARGIN)
        
    def submit(self):
        try: user = str(self.usersVariable.get())
        except:
            showinfo(
                title='Error',
                message=f'Please select a user'
            )
        else:
            self.handler.clearDoinks(user)
            showinfo(
                title='Big Success!',
                message=f'{user} has been cleared'
            )
            self.destroy()

# View db window
class ViewDB(GUI_template):
    def __init__(self, title):
        self.handler = dbHandler.Handler(DB_FILE_PATH)
        self.people = self.handler.getUsers()
        self.settings = dbHandler.Handler(file_path=SETTINGS_FILE_PATH).__dump__()
        
        GUI_template.__init__(self, title=title)
        
    def createWidgets(self):
        self.rootframe = Frame(self)
        
        ## IF NO USERS ##
        if not self.people:
            self.error_title = Label(self.rootframe, text="-- Error --\nNo users", bd=5)
            self.error_title.grid(padx=20,pady=10)
            self.gridWidgets()
            return

        for no,person in enumerate(self.people):
            ## PERSON TITLE INIT, CONFIG and GRID
            self.person_title = Label(self.rootframe, text=str(person))
            try: self.person_title.config(font=("Futura", 22))
            except: self.person_title.config(font=("Arial", 22))
            self.person_title.grid(row=0,column=no,padx=MARGIN-5,pady=MARGIN-5)
        
            # GENERATE LIST OF FORMATTED STRINGS CONTAINING ALL PERSONS SESH's
            person_sessions = [f'{sesh["date"]} {sesh["time"]}    Smokes: {sesh["smokes"]} Weed: {sesh["weed"]}g' for sesh in self.handler.getDoinks(person)]
            
            self.scrollbox = ScrollBox(master=self.rootframe, elements=person_sessions, x=False)
            self.scrollbox.grid(row=1,column=no,padx=MARGIN-5,pady=MARGIN-5)
            
            # COST LABEL
            if self.settings['show_cost']:
                weed, smokes = self.handler.getValue(person)
                self.cost_label = Label(self.rootframe, text=f'Weed: {weed} kr.\tSmokes: {smokes} kr.')
                self.cost_label.config(font=("Futura", 12))
                self.cost_label.grid(row=2, column=no)
        
        
        self.quitBtn = Button(self.rootframe, text="Exit",command=self.destroy)
        self.quitBtn.grid(column=len(self.people)-1,row=3,sticky="E")
        self.gridWidgets()
            
    def gridWidgets(self):
        self.rootframe.pack(padx=MARGIN,pady=MARGIN)

# Settings window
class Settings(GUI_template):
    
    def __init__(self, title):
        self.handler = dbHandler.Handler(file_path=SETTINGS_FILE_PATH)
        self.settings = self.handler.__dump__()
        GUI_template.__init__(self, title)
    
    def createWidgets(self):
        self.mainframe = Frame(self)
        
        # wed
        self.weed_cost = DoubleVar()
        self.weed_cost.set(self.settings['weed_cost'])
        self.weedCostLabel = Label(self.mainframe, text="Weed cost")
        self.weedCostEntry = Entry(self.mainframe, textvariable=self.weed_cost)
        
        # smok
        self.smoke_cost = DoubleVar()
        self.smoke_cost.set(self.settings['smoke_cost'])
        self.smokeCostLabel = Label(self.mainframe, text="Smoke cost")
        self.smokeCostEntry = Entry(self.mainframe, textvariable=self.smoke_cost)
        
        # show cost
        self.show_cost = IntVar()
        self.show_cost.set(self.settings["show_cost"])
        self.showCostButton = Checkbutton(self.mainframe, text="Show total debt in database", variable=self.show_cost)
        
        # apply btn
        self.saveButton = Button(self.mainframe, text="Save", command=self.submit)
        self.gridWidgets()
        
    def gridWidgets(self):
        self.weedCostLabel.grid(column= 0,row=0)
        self.weedCostEntry.grid(column=1,row=0)
        
        self.smokeCostLabel.grid(column=0,row=1)
        self.smokeCostEntry.grid(column=1,row=1)
        
        self.showCostButton.grid(columnspan=2, row=2)
        self.saveButton.grid(columnspan=2, row=3)
        
        self.mainframe.grid(padx=MARGIN,pady=MARGIN)
        
    def submit(self):        
        weed, smoke, show_cost = 0.0,0.0,1
        try: 
            weed = float(self.weed_cost.get())
            smoke = float(self.smoke_cost.get())
            show_cost = int(self.show_cost.get())
            
        except: 
            print("Error! Please use decimal point numbers")
            return
        
        else:
            settings = {
            "weed_cost": weed,
            "smoke_cost": smoke,
            "show_cost": show_cost
        }
        self.handler.__load__(settings)
        self.destroy()
 
### TEST ###
if __name__=="__main__":
    print("Running testing environment...")
    root = Tk()
    app = MainGUI(master=root)
    root.title("WUBBBA")
    root.mainloop()