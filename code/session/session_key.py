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

import csv
import json
import os
from os.path import exists
import random

# Session Anonymization Key
class SessionKey:

    _DEBUG = False

    # configuration file to be used to generate the keys
    _CONFIG_FILE_NAME = "../../config/session-config.json"

    # key file with randomly generated keys for sessions
    # 
    _KEY_FILE_NAME_TXT = "../../key/sessionKeys.txt"
    _KEY_FILE_NAME_CSV = "../../key/sessionKeys.csv"

    # a map between a session (i.e. semester) and its anonymized code
    # example (200040, 198) will link Summer semester in 2000 with the code 198
    _dictionarySession = {}
    _dictionaryKey = {}
    _dictionaryType = None

    _startYear = 0
    _endYear = 0
    _startKey = 0
    _minStep = 0
    _maxStep = 0
    _semesters = []
    _regenerate = None

    # load the configuration file for the session key
    def __loadConfig(self):
        configFile = open(self._CONFIG_FILE_NAME, )
        configData = json.load(configFile)

        self._dictionaryType = configData['format']
        self._startYear = configData['start_year']
        self._endYear = configData['end_year']
        self._startKey = configData['start_key']
        self._minStep = configData['min_step']
        self._maxStep = configData['max_step']
        self._semesters = configData['semesters_list']
        self._regenerate = configData['regenerate']

    # load the generated key file and initialize the dictionary
    # return true if succeeds, false otherwise
    def __load(self):
        file = None
        if self._dictionaryType == "TXT" and exists(self._KEY_FILE_NAME_TXT):
            file = open(self._KEY_FILE_NAME_TXT)
            lines = file.readlines()
            for line in lines:
                parts = line.split(" ")
                self._dictionarySession[int(parts[0])] = int(parts[1])
                self._dictionaryKey[int(parts[1])] = int(parts[0])
            file.close()
            if self._DEBUG:
                print("  - text file loaded: "+self._KEY_FILE_NAME_TXT)
            return True
        if self._dictionaryType == "CSV" and exists(self._KEY_FILE_NAME_CSV):
            file = open(self._KEY_FILE_NAME_CSV, mode='r')
            csvFile = csv.reader(file)
            lineIndex = 0
            sessionCode = None
            sessionKey = None
            for lines in csvFile:
                for line in lines:
                    # if self._DEBUG:
                        # print("  --- "+line)
                    lineIndex += 1
                    if lineIndex>2:
                        if lineIndex % 2 == 1:
                            sessionCode = int(line)
                            # print("sessionCode="+str(sessionCode))
                        else:
                            # print("sessionCode="+str(sessionCode))
                            sessionKey = int (line)
                            # print("sessionKey="+str(sessionKey))
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
        if os.path.exists(self._KEY_FILE_NAME_TXT):
            os.remove(self._KEY_FILE_NAME_TXT)
        if os.path.exists(self._KEY_FILE_NAME_CSV):
            os.remove(self._KEY_FILE_NAME_CSV)        
        if self._dictionaryType=="TXT":
            file = open(self._KEY_FILE_NAME_TXT, "w")
            for keyName in sorted(self._dictionarySession.keys()):
                file.write(str(keyName) + " " + str(self._dictionarySession[keyName]) + "\n")
            file.close()
            if self._DEBUG:
                print("  - text file saved: "+self._KEY_FILE_NAME_TXT)
            return True
        if self._dictionaryType=="CSV":
            # writing to the csv file 
            csvfile = open(self._KEY_FILE_NAME_CSV, "w") 
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
            header = [ "session", "key"]
            csvwriter.writerow(header)  
            # writing the fields 
            for keyName in sorted(self._dictionarySession.keys()):
                entry = [ keyName, self._dictionarySession[keyName] ]
                csvwriter.writerow(entry) 
            csvfile.close()
            if self._DEBUG:
                print("  - csv file saved: "+self._KEY_FILE_NAME_CSV)
            return True
        print("  - error saving dictionary")
        return False

    # generate a new dictionary (assumed empty)
    def __generate(self):
        lastKey =  self._startKey
        # for all years in the configuration range
        for i in range(self._startYear, self._endYear + 1):
            # for all the semesters
            for sem in self._semesters:
                # update the last key to a new valid key
                sessionCode = i * 100 + sem
                lastKey += random.randint(self._minStep, self._maxStep)
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
        if self._regenerate or not self.__load():
            self.__generate()
            self.__save()


    def getSessionKey(self,sessionCode):
        return self._dictionarySession[sessionCode]

    def getSessionCode(self,sessionKey):
        return self._dictionaryKey[sessionKey]