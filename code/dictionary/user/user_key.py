# Maintained by Mihai Boicu 

import csv
import json
import os
import random
import sys

# Anonymization of the User IDs
class UserKey:
    
    _DEBUG = False

    _projectPath = None

    # configuration constants
    _dictionaryType = None
    _regenerate = None
    _minKey = None
    _maxKey = None
    _spaceReplacement = None # = "~|~"

    # key file with randomly generated keys for sections
    _txtKeyFilename = "../key/userKeys.txt"
    _csvKeyFilename = "../key/userKeys.csv"

    _dictionaryUser = {}
    _dictionaryKey = {}

    _isModified = False
    _multiplier = 1

    # load the configuration file for the user key
    def __loadConfig(self):
        configFile = open(self._projectPath+"/config/user.json", mode='r')
        configData = json.load(configFile)
        configFile.close()

        self._dictionaryType = configData['format']
        self._regenerate = configData['regenerate']
        self._multiplier = configData['multiplier'] 
        self._minKey = configData['min-key']    
        self._maxKey = configData['max-key'] 
        self._spaceReplacement = configData['space-replacement']   

    def __cleanFiles(self):
        if self._regenerate or self._dictionaryType == "CSV":
            if os.path.exists(self._txtKeyFilename):
                os.remove(self._txtKeyFilename)
        if self._regenerate or self._dictionaryType == "TXT":
            if os.path.exists(self._csvKeyFilename):
                os.remove(self._csvKeyFilename) 

    # load the current anonymization file and initialize the dictionary
    def __load(self):
        if self._regenerate:
            return False    
        if os.path.exists(self._txtKeyFilename):
            file = open(self._txtKeyFilename, mode='r')
            lines = file.readlines()
            for line in lines:
                parts = line.split(" ")
                lastName = str(parts[0]).replace(self._spaceReplacement, " ")
                firstName = str(parts[1]).replace(self._spaceReplacement, " ")
                emailId = str(parts[2])
                key = int(parts[3])
                self._dictionaryUser[emailId] = [ lastName, firstName, key]
                self._dictionaryKey[key] = emailId
            file.close()
            if self._DEBUG:
                print("  - text file loaded: "+self._txtKeyFilename)
            return True
        if os.path.exists(self._csvKeyFilename):
            file = open(self._csvKeyFilename, mode='r')
            csvFile = csv.reader(file)
            lineIndex = 0
            lastName = None
            firstName = None
            emailId = None
            linelen = 3 + self._multiplier
            keys = []       
            for lines in csvFile:
                for line in lines:
                    lineIndex += 1
                    if lineIndex>linelen:
                        if lineIndex % linelen == 1:
                            lastName = str(line)
                        elif lineIndex % linelen == 2:
                            firstName = str(line)
                        elif lineIndex % linelen == 3:
                            emailId = str(line)
                        else:
                            key = int (line)
                            keys.append(key)
                            if lineIndex % linelen == 0:
                                self._dictionaryUser[emailId] = [ lastName, firstName, keys]
                                for key in keys:
                                    self._dictionaryKey[key] = emailId                
            if self._DEBUG:
                print("  - csv file loaded: "+self._csvKeyFilename)
                print(self._dictionaryUser)
                print(self._dictionaryKey)
            return True
        # otherwise no file
        print("  - dictionary file not found")
        return False    

    # save the current dictionary in the key file 
    def save(self):
        if not self._isModified:
            return
        if self._dictionaryType=="TXT":
            file = open(self._txtKeyFilename, "w")
            for emailId in sorted(self._dictionaryUser.keys()):
                record = self._dictionaryUser[emailId]
                lastName = record[0].replace(" ", self._spaceReplacement)
                firstName = record[1].replace(" ", self._spaceReplacement)
                txtLine  = str(lastName) + " " + str(firstName) + " " + str(emailId) 
                keys = record[2]
                for key in keys:
                    txtLine = txtLine + " " + str(key)
                file.write( txtLine + "\n")
            file.close()
            if self._DEBUG:
                print("  - text file saved: "+self._txtKeyFilename)
            return True
        if self._dictionaryType=="CSV":
            # writing to the csv file 
            csvfile = open(self._csvKeyFilename, "w") 
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
            header = [ "last name", "first name", "email id"]
            for i in range(1,self._multiplier+1):
                header.append("user key "+str(i))
            csvwriter.writerow(header)  
            # writing the fields 
            for emailId in sorted(self._dictionaryUser.keys()):
                record = self._dictionaryUser[emailId]
                entry = [ record[0], record[1], emailId]
                for key in record[2]:
                    entry.append(key)
                csvwriter.writerow(entry) 
            csvfile.close()
            if self._DEBUG:
                print("  - csv file saved: "+self._csvKeyFilename)
            return True
        print("  - error saving dictionary")
        return False

    def getMultiplication(self):
        return self._multiplier

    def getUserKeys(self, emailId):
        return self.getUserKeysFull(None, None, emailId)

    # return the existing key for the given user, if any 
    # or create and return a snew key
    def getUserKeysFull(self, lastName, firstName, emailId):
        # return current key if section already defined in dictionary
        record = self._dictionaryUser.get(emailId)
        if record != None:
            saveRecord = False
            if record[0] == None and lastName!=None:
                record[0] = lastName
                saveRecord = True
            if record[1] == None and firstName!=None:
                record[1] = firstName
                saveRecord = True
            if saveRecord:
                self._dictionaryUser[emailId] = record    
                self._isModified = True
            return record[2]
        # define new code
        
        userKeys=[]
        for i in range(1,self._multiplier+1):
            # randomly generate a new (not used) anonymized value for the user key between  min and max 
            userKey = -1
            trial = 0
            while True:
                userKey = self._minKey + (int)(random.random() * (self._maxKey - self._minKey + 1))
                if self._dictionaryKey.get(userKey) == None:
                    break
                trial += 1
                if trial > 100:
                    print("Too high density of user keys.")
                    sys.exit(1)
            userKeys.append(userKey)              
        # save the value in the dictionary
        self._dictionaryUser[emailId] = [lastName, firstName, userKeys]
        for userKey in userKeys:
            self._dictionaryKey[userKey] = emailId
        self._isModified=True
        # return the generated code
        # print("Dictionary "+str(self._dictionaryUser))
        return userKeys

    def getUserCode(self,userKey):
        return self._dictionaryKey.get(userKey)        


    # Initialize the section key based on the saved key file, if any
    def __init__(self, projectPath):
        if self._DEBUG:
            print("User dictionary initialization: ")
        self._projectPath=projectPath
        self._txtKeyFilename = projectPath + "/key/userKeys.txt"
        self._csvKeyFilename = projectPath + "/key/userKeys.csv"        
        self.__loadConfig()
        self.__cleanFiles()
        self.__load()

 