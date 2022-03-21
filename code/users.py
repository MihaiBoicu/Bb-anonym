#To anonymize the users this class is used. 
#It starts with loadConfig where it reads the json file and sets minuser code and maxuser code based on the values defined in the json file.
#If it has a userskey.txt file it loads it by reading the file line by line and storing it into a dictionary as key value pairs.  The same will next be saved by sorting the keys and then combining keys and values to a single item back to the userkeys.txt
#To generate an id, it first checks if the section is already present, if it is present the same id has been returned. If not a new value is generated by capturing a random integer value betweeen the min and max user codes. It checks if that random value is present 
#in the dictionary, the value is set  to be new code if it is present. 
#The values are then printed

class UserKey:
    configFileName = "../config/user-config.json"
    keyFileName = "../key/userKeys.txt"
    minUserCode=None
    maxUserCode=None

    dictionary = {}

    def loadConfig(self):
        userConfigFile = open(self.configFileName)
        userConfigData = json.load(userConfigFile)
        self.minUserCode = userConfigData['min_key']
        self.maxUserCode = userConfigData['max_key']
        userConfigFile.close()

    def load(self):
        # print("Grabbing User Keys!")
        file = open(self.keyFileName)
        lines = file.readlines()
        for line in lines:
            elements = line.split(' ')
            self.dictionary[(elements[0])] = int(elements[1])
        file.close()

    def save(self):
        file = open(self.keyFileName, "w")
        for keyName in sorted(self.dictionary.keys()):
            file.write(str(keyName) + " " + str(self.dictionary[keyName]) + "\n")
        file.close()

    def __init__(self):
        self.loadConfig()
        if os.path.isfile(self.keyFileName):
            self.load()

    def get(self, id):
        # check if section already used in sectionDict
        if id in self.dictionary.keys():
            return self.dictionary[id]
        # define new code              
        while True:
            code = random.randint(self.minUserCode, self.maxUserCode)
            if not code in self.dictionary.values():
                break
        self.dictionary[str(id)] = code
        return code

    def print(self):
        print("*****")
        print("*** USER KEY")
        print("*** User Key Config ***")
        print("Min User Code: "+str(self.minUserCode))
        print("Max User Code: "+str(self.maxUserCode))