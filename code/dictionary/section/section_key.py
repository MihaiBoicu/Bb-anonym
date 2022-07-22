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

    # configuration file to be used to generate the keys
    _CONFIG_FILE_NAME = "../config/section_config.json"

    # configuration constants
    _DICTIONARY_TYPE = None
    _REGENERATE = None
    _MAX_SECTIONS_PER_SESSION = None

    # key file with randomly generated keys for sections
    _KEY_FILE_NAME_TXT = "../key/sectionKeys.txt"
    _KEY_FILE_NAME_CSV = "../key/sectionKeys.csv"

    # the session anonymization key
    _sessionKey: session_key.SessionKey

    # a map between a section code in a given semester and its anonymized code
    # example "11233.202110" is associated with 12345 where 123 is the code for session 202110 and 45 is the code for section 11233
    _dictionarySection = {}
    _dictionaryKey = {}

    _isModified = False

    # load the configuration file for the section key
    def __loadConfig(self):
        configFile = open(self._CONFIG_FILE_NAME, )
        configData = json.load(configFile)
        self._DICTIONARY_TYPE = configData['format']
        self._REGENERATE = configData['regenerate']
        self._MAX_SECTIONS_PER_SESSION = configData['max_sections_per_session']

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
                self._dictionarySection[str(parts[0])] = int(parts[1])
                self._dictionaryKey[int(parts[1])] = str(parts[0])
            file.close()
            if self._DEBUG:
                print("  - text file loaded: "+self._KEY_FILE_NAME_TXT)
            return True
        if os.path.exists(self._KEY_FILE_NAME_CSV):
            file = open(self._KEY_FILE_NAME_CSV, mode='r')
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
                print("  - csv file loaded: "+self._KEY_FILE_NAME_CSV)
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
        if self._DICTIONARY_TYPE=="TXT":
            file = open(self._KEY_FILE_NAME_TXT, "w")
            for sectionCode in sorted(self._dictionarySection.keys()):
                file.write(str(sectionCode) + " " + str(self._dictionarySection[sectionCode]) + "\n")
            file.close()
            if self._DEBUG:
                print("  - text file saved: "+self._KEY_FILE_NAME_TXT)
            return True
        if self._DICTIONARY_TYPE=="CSV":
            # writing to the csv file 
            csvfile = open(self._KEY_FILE_NAME_CSV, "w") 
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
                print("  - csv file saved: "+self._KEY_FILE_NAME_CSV)
            return True
        print("  - error saving dictionary")
        return False

    # Initialize the section key based on the saved key file, if any
    def __init__(self, sessionKey):
        if self._DEBUG:
            print("Section dictionary initialization: ")
        self._sessionKey = sessionKey
        self.__loadConfig()
        self.__cleanFiles()
        self.__load()

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
            sectionKey = int(sessionKey * self._MAX_SECTIONS_PER_SESSION + (int)(random.random() * self._MAX_SECTIONS_PER_SESSION))
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

