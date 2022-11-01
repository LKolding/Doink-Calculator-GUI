from tkinter import *
from listboxscroll import ScrollBox

import dbHandler

MARGIN = 10
DB_FILE_PATH = "db.json"

class GUI_template(Toplevel):
    def __init__(self, title):
        Toplevel.__init__(self)
        self.title(title)
        self.resizable(FALSE, FALSE)
        self.createWidgets()
    
    def createWidgets(self): '''both creates and grids widgets'''
    def gridWidgets(self): '''DEPRECIATED, YET STILL IN USE, GL UNDERSTANDING THIS'''

# Main menu window
class MainGUI(GUI_template):
    
    def __init__(self, title): GUI_template.__init__(self, title)
    
    def createWidgets(self):
        self.topframe = Frame(self)
        self.leftframe = Frame(self)
        self.rightframe = Frame(self)

        self.title_label = Label(self.topframe, text='Doink Calculator')

        self.view_db_button = Button(self.leftframe,text="View DB", command=self.viewDBWindow)
        self.add_person_button = Button(self.rightframe,text="Add person",  command=self.addPersonWindow)
        self.add_doink_button = Button(self.leftframe,text="Add doink",  command=self.addDoinkWindow)
        self.clear_person_button = Button(self.rightframe,text="Clear person",  command=self.clearPersonWindow)
        self.settings_button = Button(self.leftframe,text="Settings",  command=self.settingsWindow)
        self.quit_button = Button(self.rightframe,text="Quit",  command=exit)
        self.gridWidgets()

    def gridWidgets(self):
        self.title_label.pack()

        self.view_db_button.pack()
        self.add_person_button.pack()
        self.add_doink_button.pack()
        self.clear_person_button.pack()
        self.settings_button.pack()
        self.quit_button.pack()

        self.topframe.pack(side=TOP, padx=MARGIN,pady=MARGIN)
        self.leftframe.pack(side=LEFT, padx=MARGIN,pady=MARGIN)
        self.rightframe.pack(side=RIGHT, padx=MARGIN,pady=MARGIN)

    def viewDBWindow(self):
        # init and display db window
        dad = ViewDB("Database")
        
    def addPersonWindow(self):
        # init and display add person dialog
        dad = AddPerson("Add person")
        
    def addDoinkWindow(self):
        # init and display adddoink dialog
        dad = AddDoink(title="Add Doink")
        
    def clearPersonWindow(self):
        # init and display clear person window
        dad = ClearPerson("Clear person")
        
    def settingsWindow(self):
        dad = Settings("Settings")

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
        weed = float(self.weed_entry.get())
        smokes = float(self.smokes_entry.get())
        user = self.users_list.get(self.users_list.curselection())
        self.handler.saveDoink(user, smokes, weed)

# Add person dialog
class AddPerson(GUI_template):
    def createWidgets(self):
        self.name_entry = Entry(self, text="name")
        self.add_person_button = Button(self, text="Add")
        self.gridWidgets()
        
    def gridWidgets(self):
        self.name_entry.pack(padx=MARGIN,pady=MARGIN)
        self.add_person_button.pack(padx=MARGIN,pady=MARGIN)

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
            self.person_title = Label(self.rootframe, text=str(person))
            self.person_title.grid(row=0,column=no,padx=MARGIN-5,pady=MARGIN-5)
            
            person_sessions = []
            for sesh in self.handler.getDoinks(person): person_sessions.append(str(f'{sesh["date"]} {sesh["time"]} Smokes: {sesh["smokes"]} Weed: {sesh["weed"]}g'))
            
            self.scrollbox = ScrollBox(master=self.rootframe, elements=person_sessions)
            self.scrollbox.grid(row=1,column=no,padx=MARGIN-5,pady=MARGIN-5)
        
        self.remove_button = Button(self.controls_frame, text="Remove").grid()
        
        self.gridWidgets()
            
    def gridWidgets(self):
        self.rootframe.pack(padx=MARGIN,pady=MARGIN)
        self.controls_frame.pack(padx=MARGIN, pady=MARGIN)

# Settings window
class Settings(GUI_template):
    def createWidgets(self):
        self.mainframe = Frame(self)
        self.weedCostLabel = Label(self.mainframe, text="Weed cost:")
        self.weedCostEntry = Entry(self.mainframe)
        self.smokeCostLabel = Label(self.mainframe, text="Smoke cost:")
        self.smokeCostEntry = Entry(self.mainframe)
        self.saveButton = Button(self.mainframe, text="Save")
        self.gridWidgets()
        
    def gridWidgets(self):
        self.weedCostLabel.pack(padx=MARGIN,pady=MARGIN)
        self.weedCostEntry.pack(padx=MARGIN,pady=MARGIN)
        self.smokeCostLabel.pack(padx=MARGIN,pady=MARGIN)
        self.smokeCostEntry.pack(padx=MARGIN,pady=MARGIN)
        self.saveButton.pack(padx=MARGIN,pady=MARGIN)
        self.mainframe.pack(padx=MARGIN,pady=MARGIN)