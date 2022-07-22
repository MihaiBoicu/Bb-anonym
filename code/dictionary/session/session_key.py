# Compiled and maintained by Mihai Boicu 
# 2021 July-August
# - David Liu (a1.py, a2.py gc processing)
# - Anish Malik (a3.py - qr processing)
# - Mihai Boicu (general design and convert to classes)
# 2022 March-April
# - Anushree Manoharrao (session-key.py - documentation,comments)
# - Mouhamed Sylla (comment code)
# - Mihai Boicu (update code/comments for clarity)
# 2022 July 
# - Mihai Boicu (add CSV output format for keys)
# - Mihai Boicu (add regenerate option, invalid values and cleanup files)

import csv
import json
import os
import random

# Session Anonymization Key
class SessionKey:

    _DEBUG = False

    # configuration file to be used to generate the keys
    _CONFIG_FILE_NAME = "../config/session-config.json"

    # configuration constants
    _START_YEAR = 0
    _END_YEAR = 0
    _START_KEY = 0
    _MIN_STEP = 0
    _MAX_STEP = 0
    _SEMESTERS = []
    _DICTIONARY_TYPE = None
    _REGENERATE = None

    # key file with randomly generated keys for sessions
    _KEY_FILE_NAME_TXT = "../key/sessionKeys.txt"
    _KEY_FILE_NAME_CSV = "../key/sessionKeys.csv"
    

    # a map between a session (i.e. semester) and its anonymized code
    # example (200040, 198) will link Summer semester in 2000 with the code 198
    _dictionarySession = {}
    _dictionaryKey = {}

    # load the configuration file for the session key
    def __loadConfig(self):
        configFile = open(self._CONFIG_FILE_NAME, )
        configData = json.load(configFile)

        self._DICTIONARY_TYPE = configData['format']
        self._START_YEAR = configData['start_year']
        self._END_YEAR = configData['end_year']
        self._START_KEY = configData['start_key']
        self._MIN_STEP = configData['min_step']
        self._MAX_STEP = configData['max_step']
        self._SEMESTERS = configData['semesters_list']
        self._REGENERATE = configData['regenerate']

    def __cleanFiles(self):
        if self._REGENERATE or self._DICTIONARY_TYPE == "CSV":
            if os.path.exists(self._KEY_FILE_NAME_TXT):
                os.remove(self._KEY_FILE_NAME_TXT)
        if self._REGENERATE or self._DICTIONARY_TYPE == "TXT":
            if os.path.exists(self._KEY_FILE_NAME_CSV):
                os.remove(self._KEY_FILE_NAME_CSV) 

    # load the generated key file and initialize the dictionary
    # return true if succeeds, false otherwise
    def __load(self):
        if self._REGENERATE:
            return False
        if os.path.exists(self._KEY_FILE_NAME_TXT):
            file = open(self._KEY_FILE_NAME_TXT, mode="r")
            lines = file.readlines()
            for line in lines:
                parts = line.split(" ")
                self._dictionarySession[int(parts[0])] = int(parts[1])
                self._dictionaryKey[int(parts[1])] = int(parts[0])
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
                            self._dictionarySession[sessionCode] = sessionKey
                            self._dictionaryKey[sessionKey] = sessionCode
            file.close()
            if self._DEBUG:
                print("  - csv file loaded: "+self._KEY_FILE_NAME_CSV)
                print(self._dictionarySession)
                print(self._dictionaryKey)
            return True
        # otherwise no file
        print("  - dictionary file not found")
        return False
        
    # save the key file based on the current dictionary
    # return true if succeeds, false otherwise
    def __save(self):      
        if self._DICTIONARY_TYPE=="TXT":
            file = open(self._KEY_FILE_NAME_TXT, "w")
            for sessionCode in sorted(self._dictionarySession.keys()):
                file.write(str(sessionCode) + " " + str(self._dictionarySession[sessionCode]) + "\n")
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
            for sessionCode in sorted(self._dictionarySession.keys()):
                entry = [ sessionCode, self._dictionarySession[sessionCode] ]
                csvwriter.writerow(entry) 
            csvfile.close()
            if self._DEBUG:
                print("  - csv file saved: "+self._KEY_FILE_NAME_CSV)
            return True
        print("  - error saving dictionary")
        return False

    # generate a new dictionary (assumed empty)
    def __generate(self):
        lastKey =  self._START_KEY
        # for all years in the configuration range
        for i in range(self._START_YEAR, self._END_YEAR + 1):
            # for all the semesters
            for sem in self._SEMESTERS:
                # update the last key to a new valid key
                sessionCode = i * 100 + sem
                lastKey += random.randint(self._MIN_STEP, self._MAX_STEP)
                # save the semester and key in dictionary
                self._dictionarySession[sessionCode] = lastKey
                self._dictionaryKey[lastKey] = sessionCode
        if self._DEBUG:
            print("  - random key dictionary generated")
        # debug info
        # print("lastKey: ",lastKey)
        # print("sessionDict: ", sessionDict)

    # initialize the class
    # load the keys in dictionary if key file exist
    # or generate and save the key file otherwise
    def __init__(self):
        if self._DEBUG:
            print("Session dictionary initialization: ")
        self.__loadConfig()
        self.__cleanFiles()
        if not self.__load():
            self.__generate()
            self.__save()


    def getSessionKey(self,sessionCode):
        return self._dictionarySession.get(sessionCode)

    def getSessionCode(self,sessionKey):
        return self._dictionaryKey.get(sessionKey)