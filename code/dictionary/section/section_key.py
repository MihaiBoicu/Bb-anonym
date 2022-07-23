# Maintained by Mihai Boicu based on code created by:
# 2021 July-August
# - David Liu (a1.py, a2.py gc processing)
# - Anish Malik (a3.py - qr processing)
# 2022 March-April
# - Mouhamed Syllas (extract code and comment)
# - Mihai Boicu (update code/comments for clarity)
# 2022 July
# - Mihai Boicu (add CSV output format for keys)
# - Mihai Boicu (add regenerate option, invalid values and cleanup files)

import csv
import json
import os
import random
from dictionary.session import session_key
import sys

# Anonymization of the Section Codes
class SectionKey:

    _DEBUG = False

    _projectPath = None

    # configuration constants
    _dictionaryType = None
    _regenerate = None
    _maxSectionsPerSession = None

    # key file with randomly generated keys for sections
    _txtKeyFilename: None
    _csvKeyFilename: None  


    # the session anonymization key
    _sessionKey: session_key.SessionKey

    # a map between a section code in a given semester and its anonymized code
    # example "11233.202110" is associated with 12345 where 123 is the code for session 202110 and 45 is the code for section 11233
    _dictionarySection = {}
    _dictionaryKey = {}

    _isModified = False

    # load the configuration file for the section key
    def __loadConfig(self):
        configFile = open(self._projectPath+"/config/section.json", mode='r')
        configData = json.load(configFile)
        configFile.close()
        self._dictionaryType = configData['format']
        self._regenerate = configData['regenerate']
        self._maxSectionsPerSession = configData['max_sections_per_session']

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
                self._dictionarySection[str(parts[0])] = int(parts[1])
                self._dictionaryKey[int(parts[1])] = str(parts[0])
            file.close()
            if self._DEBUG:
                print("  - text file loaded: "+self._txtKeyFilename)
            return True
        if os.path.exists(self._csvKeyFilename):
            file = open(self._csvKeyFilename, mode='r')
            csvFile = csv.reader(file)
            lineIndex = 0
            sessionCode = None
            sessionKey = None
            for lines in csvFile:
                for line in lines:
                    lineIndex += 1
                    if lineIndex>2:
                        if lineIndex % 2 == 1:
                            sessionCode = int(line)
                        else:
                            sessionKey = int (line)
                            self._dictionarySection[sessionCode] = sessionKey
                            self._dictionaryKey[sessionKey] = sessionCode
            file.close()
            if self._DEBUG:
                print("  - csv file loaded: "+self._csvKeyFilename)
                print(self._dictionarySection)
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
            for sectionCode in sorted(self._dictionarySection.keys()):
                file.write(str(sectionCode) + " " + str(self._dictionarySection[sectionCode]) + "\n")
            file.close()
            if self._DEBUG:
                print("  - text file saved: "+self._txtKeyFilename)
            return True
        if self._dictionaryType=="CSV":
            # writing to the csv file 
            csvfile = open(self._csvKeyFilename, "w") 
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
            header = [ "session", "key"]
            csvwriter.writerow(header)  
            # writing the fields 
            for sectionCode in sorted(self._dictionarySection.keys()):
                entry = [ sectionCode, self._dictionarySection[sectionCode] ]
                csvwriter.writerow(entry) 
            csvfile.close()
            if self._DEBUG:
                print("  - csv file saved: "+self._csvKeyFilename)
            return True
        print("  - error saving dictionary")
        return False

    # return the existing key for the given section, if any 
    # or create and return a new key
    def getSectionKey(self, sectionCode):
        # return current key if section already defined in dictionary
        sectionKey = self._dictionarySection.get(sectionCode)
        if sectionKey != None:
            return sectionKey
        # define new code
        # identify the session in section name
        # i.e.  202110 in "11233.202110"
        parts = sectionCode.split(".")
        sectionNumber = int(parts[0])
        sessionCode = int(parts[1])
        sessionKey = self._sessionKey.getSessionKey(sessionCode)
        if sessionKey==None:
            print("Invalid session code for this section: "+str(sectionCode))
            sys.exit(1)
        # randomly generate a new (not used) anonymized value for the section key grouping the sections in the same session together 
        sectionKey = -1
        trial = 0
        while True:
            sectionKey = int(sessionKey * self._maxSectionsPerSession + (int)(random.random() * self._maxSectionsPerSession))
            if self._dictionaryKey.get(sectionKey) == None:
                break
            trial += 1
            if trial > 100:
                print("Too high density of section keys per session.")
                sys.exit(1)                
        # save the value in the dictionary
        self._dictionarySection[sectionCode] = sectionKey
        self._dictionaryKey[sectionKey] = sectionCode
        self._isModified=True
        # return the generated code
        return self._dictionarySection.get(sectionCode)

    def getSectionCode(self,sectionKey):
        return self._dictionaryKey.get(sectionKey)

    def __init__(self, projectPath, sessionKey):
        if self._DEBUG:
            print("Section dictionary initialization: ")
        self._sessionKey = sessionKey            
        self._projectPath = projectPath
        self._txtKeyFilename = projectPath + "/key/sectionKeys.txt"
        self._csvKeyFilename = projectPath +"/key/sectionKeys.csv"
        self.__loadConfig()
        self.__cleanFiles()
        self.__load()