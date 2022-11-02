from datetime import datetime
import json
import os

READ_MODE = "r"
WRITE_MODE = "w"

class Handler:
    '''Handler to hold one specific json file (self.file_name) and handle reading and writing to it'''
    def __init__(self, file_path): 
            self.file_name = file_path
            self.init_file(self.file_name)
    
    def init_file(self, file_name):
        '''creates file _if_ it doesn't exist'''
        if not os.path.isfile(file_name): 
                with open(file_name, "w") as f:
                    f.write(json.dumps({}, indent=4, sort_keys=True))

    def saveDoink(self, person: str, smokes: float, weed: float) -> bool:
        '''Returns true if succesfull, false if otherwise'''
        # Variable to hold object once decoded from json file
        db: object = ""

        ## READ AND DECODE CONTENTS OF FILE
        with open(self.file_name, READ_MODE) as f:
            ## READ
            file_content = f.read()
            if file_content == "" or file_content == None: raise Exception("Empty database")
            ## DECODE
            db = json.loads(file_content)

        ## CHECK IF PERSON EXISTS
        people = []
        for guy in db: people.append(guy)
        if person not in people: raise Exception(f"No person in database called {person}")

        # datetime object containing current date and time
        now = datetime.now()

        # dd/mm/YY H:M:S
        date = now.strftime("%d/%m/%Y")
        time = now.strftime("%H:%M:%S")

        with open(self.file_name, WRITE_MODE) as f:
            try:
                # Add new entry in person's list of sesh's
                db[person].append(
                    {
                        "date":str(date),
                        "time":str(time),
                        "smokes":float(smokes),
                        "weed":float(weed),
                    }
                )
            except Exception as e: print(f"Couldn't add new entry to list of objects\n{e}")

            ## ENCODE AND WRITE TO FILE
            try:
                ## ENCODE
                newobj = json.dumps(db, indent=4, sort_keys=True)
                ## WRITE
                f.write(newobj)
            except Exception as e: print(f"Couldn't save file\n{e}")
            
        print("Doink added!")

    def getDoinks(self, person) -> list:
        '''returns list of seshs of person. Returns false if none found'''
        with open(self.file_name, READ_MODE) as f:
            ## READ FILE
            obj = json.loads(f.read())

            ## CHECK IF PERSON EXISTS
            people = []
            for guy in obj: people.append(guy)
            if person not in people: raise Exception(f"No person in database called {person}")
            if obj[person] is None: return False
            
            return obj[person]
       
    def getUsers(self, historical=False) -> list:
        '''Returns list of users. Enable historical argument to handle historical data json file instead of default db file'''
        if not historical:
            with open(self.file_name, READ_MODE) as f:
                ## READ FILE
                obj = json.loads(f.read())
                people = []
                for guy in obj: people.append(guy)
                
                if people == [] or people == None: return False
                return people
        else:
            with open("historical_data.json", READ_MODE) as f:
                ## READ FILE
                obj = json.loads(f.read())
                people = []
                for guy in obj: people.append(guy)
                
                if people == [] or people == None: return False
                return people
            
    def clearDoinks(self, person):
        # Variable to hold decoded json object from file
        db: object 

        ## READ AND DECODE
        with open(self.file_name, READ_MODE) as f:
            ## READ
            file_content = f.read()
            if file_content == "" or file_content == None: raise Exception("Empty database")
            ## DECODE
            db = json.loads(file_content)

        ## CHECK IF PERSON EXISTS
        people = []
        for guy in db: people.append(guy)
        if person not in people: raise Exception(f"Person '{person}' doesn't exist")

        cleared_doinks = db[person]
        db[person] = []

        ## WRITE TO FILE
        with open(self.file_name, WRITE_MODE) as f: 
            ## ENCODE
            newobj = json.dumps(db, indent=4, sort_keys=True)
            ## WRITE
            f.write(newobj)

        ##
        ## SAVE HISTORICAL DATA
        ##
        # variable to hold decoded json object from file
        data: object
        # check file exists and create one if it doesn't
        if not os.path.isfile("historical_data.json"): 
            with open("historical_data.json", "w") as f:
                f.write(json.dumps({}, indent=4, sort_keys=True))
        # read file and decode json
        with open("historical_data.json", READ_MODE) as f: data = json.loads(f.read())
        
        ## CHECK IF PERSON EXISTS and ADD THEM IF THEY DON'T
        people = self.getUsers(historical=True)
        if person not in people: data[person] = []
        # add cleared doinks from db
        for doink in cleared_doinks: data[person].append(doink)
        
        # write to file
        with open("historical_data.json", WRITE_MODE) as f: 
            ## ENCODE
            newobj = json.dumps(data, indent=4, sort_keys=True)
            ## WRITE
            f.write(newobj)

        print(f"{person} has been cleared!")
            
    def getValue(self, person) -> float:
        '''Returns total cost of all of persons ledger entries. (weed, smokes) in DKK'''
        weed = 0.0
        smokes = 0.0
        
        doinks = self.getDoinks(person)
        
        for sesh in doinks:
            weed += float(sesh['weed'])
            smokes += float(sesh['smokes'])
            
        weed *= 60
        smokes *= 2.5
        
        return weed, smokes

    def addPerson(self, person):
        # Variable to hold object once decoded from json file
        db: object = ""

        ## READ AND DECODE CONTENTS OF FILE
        with open(self.file_name, READ_MODE) as f:
            ## READ
            file_content = f.read()
            if file_content == "" or file_content == None: raise Exception("Empty database")
            ## DECODE
            db = json.loads(file_content)

        ## CHECK IF PERSON EXISTS
        people = self.getUsers()
        if people != False:
            if person in people: raise Exception(f"Person '{person}' already exists")

        db[person] = []

        with open(self.file_name, WRITE_MODE) as f:
            ## ENCODE AND WRITE TO FILE
            try:
                ## ENCODE
                newobj = json.dumps(db, indent=4, sort_keys=True)
                ## WRITE
                f.write(newobj)
            except Exception as e: print(f"Couldn't save file\n{e}")
            else: print(f"{person} has been added!")

    def __dump__(self) -> dict:
        ## READ AND DECODE CONTENTS OF FILE
        with open(self.file_name, READ_MODE) as f:
            ## READ
            file_content = f.read()
            if file_content == "" or file_content == None: raise Exception("Settings empty (?)")
            ## DECODE
            return json.loads(file_content)
        
    def __load__(self, settings):
        with open(self.file_name, "w") as f:
        ## ENCODE AND WRITE TO FILE
            try:
                ## ENCODE
                newobj = json.dumps(settings, indent=4, sort_keys=True)
                ## WRITE
                f.write(newobj)
            except Exception as e: print(f"Couldn't save file '{self.file_name}'\n{e}")
        

if __name__=="__main__": 
    print("ERROR! Don't run this file. It is meant as a module")
    exit()