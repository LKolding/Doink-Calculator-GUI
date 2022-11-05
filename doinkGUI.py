from tkinter import *
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
        self.leftframe = Frame(self.frame)
        self.rightframe = Frame(self.frame)

        self.title_label = Label(self.topframe, text="Doinkydoinky")
        self.title_label.config(font=("Futura", 36))

        self.view_db_button = Button(self.leftframe,text="View DB", command=self.viewDBWindow)
        self.add_person_button = Button(self.rightframe,text="Add person",  command=self.addPersonWindow)
        self.add_doink_button = Button(self.leftframe,text="Add doink",  command=self.addDoinkWindow)
        self.clear_person_button = Button(self.rightframe,text="Clear person",  command=self.clearPersonWindow)
        self.settings_button = Button(self.leftframe,text="Settings",  command=self.settingsWindow)
        self.quit_button = Button(self.rightframe,text="Quit",  command=exit)
        self.gridWidgets()

    def gridWidgets(self):
        self.title_label.grid()

        self.view_db_button.grid(sticky="NSEW")
        self.add_person_button.grid(sticky="NSEW")
        self.add_doink_button.grid(sticky="NSEW")
        self.clear_person_button.grid(sticky="NSEW")
        self.settings_button.grid(sticky="NSEW")
        self.quit_button.grid(sticky="E")

        EXTRA_MARGIN = 15
        self.topframe.grid(row=0,columnspan=2, padx=MARGIN+EXTRA_MARGIN,pady=MARGIN+EXTRA_MARGIN)
        self.leftframe.grid(row=1, column=0, padx=MARGIN+EXTRA_MARGIN,pady=MARGIN+EXTRA_MARGIN)
        self.rightframe.grid(row=1, column=1, padx=MARGIN+EXTRA_MARGIN,pady=MARGIN+EXTRA_MARGIN)

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
        if users:
            for no,user in enumerate(users): 
                self.users_list.insert(no,user)
        else:
            self.users_list.insert(1,"NO USERS")
            
        # bottom
        self.add_doink_button = Button(self.botframe, text="Add", command=self.submit)
        self.gridWidgets()
        
    def gridWidgets(self):
        self.weed_label.pack()
        self.weed_entry.pack()
        self.smokes_label.pack()
        self.smokes_entry.pack()
        self.incl_date.pack()
        self.incl_date.select() #defaults adding date to entry
        self.users_list.pack()
        self.add_doink_button.pack()
        
        self.midframe.pack(padx=MARGIN,pady=MARGIN)
        self.botframe.pack(padx=MARGIN,pady=MARGIN)

    def submit(self):
        weed: float
        smokes: float
        user: str
        try:
            weed = float(self.weed_entry.get())
            smokes = float(self.smokes_entry.get())
        except: print("Please select weed and smokes amount")
        
        try: user = self.users_list.get(self.users_list.curselection())
        except: print("Please select user")
        self.handler.saveDoink(user, smokes, weed)
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
        try: self.handler.addPerson(str(self.name_entry.get()))
        except: raise Exception(f"Couldn't add person {self.name_entry.get()}")
        else: self.destroy()
        
# Clear person dialog
class ClearPerson(GUI_template):
    
    def __init__(self,title):
        self.handler = dbHandler.Handler(DB_FILE_PATH)
        GUI_template.__init__(self,title)
    
    def createWidgets(self):
        # LIST OF USERS
        self.users_list = Listbox(self, height=4)
        users = self.handler.getUsers()
        if users:
            for no,user in enumerate(users): 
                self.users_list.insert(no,user)
        else:
            self.users_list.insert(1,"NO USERS")
            
        self.clear_person_button = Button(self, text="Clear", command=self.submit)
        self.gridWidgets()
        
    def gridWidgets(self):
        self.users_list.pack(padx=MARGIN,pady=MARGIN)
        self.clear_person_button.pack(padx=MARGIN,pady=MARGIN)
        
    def submit(self):
        user = self.users_list.get(self.users_list.curselection())
        self.handler.clearDoinks(user)
        self.destroy()

# View db window
class ViewDB(GUI_template):
    def __init__(self, title):
        self.handler = dbHandler.Handler(DB_FILE_PATH)
        self.people = self.handler.getUsers()
        
        GUI_template.__init__(self, title=title)
        
    def createWidgets(self):
        self.rootframe = Frame(self)
        self.controls_frame = Frame(self)
        
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
            
            person_sessions = []
            for sesh in self.handler.getDoinks(person): person_sessions.append(str(f'{sesh["date"]} {sesh["time"]}    Smokes: {sesh["smokes"]} Weed: {sesh["weed"]}g'))
            
            self.scrollbox = ScrollBox(master=self.rootframe, elements=person_sessions, x=False)
            self.scrollbox.grid(row=1,column=no,padx=MARGIN-5,pady=MARGIN-5)
            
            weed, smokes = self.handler.getValue(person)
            self.cost_label = Label(self.rootframe, text=f'Weed: {weed} kr.\tSmokes: {smokes} kr.')
            self.cost_label.config(font=("Futura", 12))
            self.cost_label.grid(row=2, column=no)
        
        self.gridWidgets()
            
    def gridWidgets(self):
        self.rootframe.pack(padx=MARGIN,pady=MARGIN)
        self.controls_frame.pack(padx=MARGIN, pady=MARGIN)

# Settings window
class Settings(GUI_template):
    
    def __init__(self, title):
        self.handler = dbHandler.Handler(file_path=SETTINGS_FILE_PATH)
        self.settings = self.handler.__dump__()
        GUI_template.__init__(self, title)
    
    def createWidgets(self):
        self.mainframe = Frame(self)
        
        self.weed_cost = IntVar()
        self.weed_cost.set(self.settings['weed_cost'])
        self.weedCostLabel = Label(self.mainframe, text="Weed cost")
        self.weedCostEntry = Entry(self.mainframe, textvariable=self.weed_cost)
        
        self.smoke_cost = IntVar()
        self.smoke_cost.set(self.settings['smoke_cost'])
        self.smokeCostLabel = Label(self.mainframe, text="Smoke cost")
        self.smokeCostEntry = Entry(self.mainframe, textvariable=self.smoke_cost)
        
        self.show_cost = IntVar()
        self.show_cost.set(self.settings["show_cost"])
        self.showCostButton = Checkbutton(self.mainframe, text="Show cost", variable=self.show_cost)
        
        self.saveButton = Button(self.mainframe, text="Save", command=self.submit)
        self.gridWidgets()
        
    def gridWidgets(self):
        self.weedCostLabel.pack(padx=MARGIN,pady=MARGIN)
        self.weedCostEntry.pack(padx=MARGIN,pady=MARGIN)
        self.smokeCostLabel.pack(padx=MARGIN,pady=MARGIN)
        self.smokeCostEntry.pack(padx=MARGIN,pady=MARGIN)
        self.showCostButton.pack()
        self.saveButton.pack(padx=MARGIN,pady=MARGIN)
        self.mainframe.pack(padx=MARGIN,pady=MARGIN)
        
    def submit(self):
        settings = {
            "weed_cost": self.weed_cost.get(),
            "smoke_cost": self.smoke_cost.get(),
            "show_cost": self.show_cost.get()
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