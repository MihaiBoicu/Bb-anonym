# Maintained by Mihai Boicu 

import csv
import json
import os
import random
import sys

# Anonymization of the User IDs
class UserKey:
    
    _DEBUG = False

    # configuration file to be used to generate the keys
    _CONFIG_FILE_NAME = "../config/user-config.json"

    # configuration constants
    _DICTIONARY_TYPE = None
    _REGENERATE = None
    _MIN_KEY = None
    _MAX_KEY = None

    # key file with randomly generated keys for sections
    _KEY_FILE_NAME_TXT = "../key/userKeys.txt"
    _KEY_FILE_NAME_CSV = "../key/userKeys.csv"

    _SPACE_REPLACEMENT = "~|~"

    _dictionaryUser = {}
    _dictionaryKey = {}

    _isModified = False

    # load the configuration file for the user key
    def __loadConfig(self):
        configFile = open(self._CONFIG_FILE_NAME, )
        configData = json.load(configFile)
        self._DICTIONARY_TYPE = configData['format']
        self._REGENERATE = configData['regenerate']
        self._MIN_KEY = configData['min_key']    
        self._MAX_KEY = configData['max_key']    


    def __cleanFiles(self):
        if self._REGENERATE or self._DICTIONARY_TYPE == "CSV":
            if os.path.exists(self._KEY_FILE_NAME_TXT):
                os.remove(self._KEY_FILE_NAME_TXT)
        if self._REGENERATE or self._DICTIONARY_TYPE == "TXT":
            if os.path.exists(self._KEY_FILE_NAME_CSV):
                os.remove(self._KEY_FILE_NAME_CSV) 


    # load the current anonymization file and initialize the dictionary
    def __load(self):
        if self._REGENERATE:
            return False    
        if os.path.exists(self._KEY_FILE_NAME_TXT):
            file = open(self._KEY_FILE_NAME_TXT, mode='r')
            lines = file.readlines()
            for line in lines:
                parts = line.split(" ")
                lastName = str(parts[0]).replace(self._SPACE_REPLACEMENT, " ")
                firstName = str(parts[1]).replace(self._SPACE_REPLACEMENT, " ")
                emailId = str(parts[2])
                key = int(parts[3])
                self._dictionaryUser[emailId] = [ lastName, firstName, key]
                self._dictionaryKey[key] = emailId
            file.close()
            if self._DEBUG:
                print("  - text file loaded: "+self._KEY_FILE_NAME_TXT)
            return True
        if os.path.exists(self._KEY_FILE_NAME_CSV):
            file = open(self._KEY_FILE_NAME_CSV, mode='r')
            csvFile = csv.reader(file)
            lineIndex = 0
            lastName = None
            firstName = None
            emailId = None
            key = None           
            for lines in csvFile:
                for line in lines:
                    lineIndex += 1
                    if lineIndex>4:
                        if lineIndex % 4 == 1:
                            lastName = str(line)
                        elif lineIndex % 4 == 2:
                            firstName = str(line)
                        elif lineIndex % 4 == 3:
                            emailId = str(line)
                        else:
                            key = int (line)
                            self._dictionaryUser[emailId] = [ lastName, firstName, key]
                            self._dictionaryKey[key] = emailId
            file.close()
            if self._DEBUG:
                print("  - csv file loaded: "+self._KEY_FILE_NAME_CSV)
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
        if self._DICTIONARY_TYPE=="TXT":
            file = open(self._KEY_FILE_NAME_TXT, "w")
            for emailId in sorted(self._dictionaryUser.keys()):
                record = self._dictionaryUser[emailId]
                lastName = record[0].replace(" ", self._SPACE_REPLACEMENT)
                firstName = record[1].replace(" ", self._SPACE_REPLACEMENT)
                key = record[2]
                file.write(str(lastName) + " " + str(firstName) + " " + str(emailId) + " " + str(key) + "\n")
            file.close()
            if self._DEBUG:
                print("  - text file saved: "+self._KEY_FILE_NAME_TXT)
            return True
        if self._DICTIONARY_TYPE=="CSV":
            # writing to the csv file 
            csvfile = open(self._KEY_FILE_NAME_CSV, "w") 
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
            header = [ "last name", "first name", "email id", "user key"]
            csvwriter.writerow(header)  
            # writing the fields 
            for emailId in sorted(self._dictionaryUser.keys()):
                record = self._dictionaryUser[emailId]
                entry = [ record[0], record[1], emailId, record[2] ]
                csvwriter.writerow(entry) 
            csvfile.close()
            if self._DEBUG:
                print("  - csv file saved: "+self._KEY_FILE_NAME_CSV)
            return True
        print("  - error saving dictionary")
        return False

    # Initialize the section key based on the saved key file, if any
    def __init__(self):
        if self._DEBUG:
            print("User dictionary initialization: ")
        self.__loadConfig()
        self.__cleanFiles()
        self.__load()

    def getUserKey(self, emailId):
        return self.getUserKeyFull(None, None, emailId)

    # return the existing key for the given user, if any 
    # or create and return a new key
    def getUserKeyFull(self, lastName, firstName, emailId):
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
        
        # randomly generate a new (not used) anonymized value for the user key between  min and max 
        userKey = -1
        trial = 0
        while True:
            userKey = self._MIN_KEY + (int)(random.random() * (self._MAX_KEY - self._MIN_KEY + 1))
            if self._dictionaryKey.get(userKey) == None:
                break
            trial += 1
            if trial > 100:
                print("Too high density of user keys.")
                sys.exit(1)              
        # save the value in the dictionary
        self._dictionaryUser[emailId] = [lastName, firstName, userKey]
        self._dictionaryKey[userKey] = emailId
        self._isModified=True
        # return the generated code
        # print("Dictionary "+str(self._dictionaryUser))
        return userKey

    def getUserCode(self,userKey):
        return self._dictionaryKey.get(userKey)        

 