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
    _projectPath = None

    # configuration constants
    _startYear = 0
    _endYear = 0
    _startKey = 0
    _minStep = 0
    _maxStep = 0
    _semesters = []
    _dictionaryType = None
    _regenerate = None

    # key file with randomly generated keys for sessions
    _txtKeyFilename: None
    _csvKeyFilename: None    

    # a map between a session (i.e. semester) and its anonymized code
    # example (200040, 198) will link Summer semester in 2000 with the code 198
    _dictionarySession = {}
    _dictionaryKey = {}

    # load the configuration file for the session key
    def __loadConfig(self):
        configFile = open(self._projectPath+"/config/session.json", mode='r')
        configData = json.load(configFile)
        configFile.close()

        self._dictionaryType = configData['format']
        self._startYear = configData['start_year']
        self._endYear = configData['end_year']
        self._startKey = configData['start_key']
        self._minStep = configData['min_step']
        self._maxStep = configData['max_step']
        self._semesters = configData['semesters_list']
        self._regenerate = configData['regenerate']

    def __cleanFiles(self):
        if self._regenerate or self._dictionaryType == "CSV":
            if os.path.exists(self._txtKeyFilename):
                os.remove(self._txtKeyFilename)
        if self._regenerate or self._dictionaryType == "TXT":
            if os.path.exists(self._csvKeyFilename):
                os.remove(self._csvKeyFilename) 

    # load the generated key file and initialize the dictionary
    # return true if succeeds, false otherwise
    def __load(self):
        if self._regenerate:
            return False
        if os.path.exists(self._txtKeyFilename):
            file = open(self._txtKeyFilename, mode="r")
            lines = file.readlines()
            for line in lines:
                parts = line.split(" ")
                self._dictionarySession[int(parts[0])] = int(parts[1])
                self._dictionaryKey[int(parts[1])] = int(parts[0])
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
                            self._dictionarySession[sessionCode] = sessionKey
                            self._dictionaryKey[sessionKey] = sessionCode
            file.close()
            if self._DEBUG:
                print("  - csv file loaded: "+self._csvKeyFilename)
                print(self._dictionarySession)
                print(self._dictionaryKey)
            return True
        # otherwise no file
        print("  - dictionary file not found")
        return False
        
    # save the key file based on the current dictionary
    # return true if succeeds, false otherwise
    def __save(self):      
        if self._dictionaryType=="TXT":
            file = open(self._txtKeyFilename, "w")
            for sessionCode in sorted(self._dictionarySession.keys()):
                file.write(str(sessionCode) + " " + str(self._dictionarySession[sessionCode]) + "\n")
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
            for sessionCode in sorted(self._dictionarySession.keys()):
                entry = [ sessionCode, self._dictionarySession[sessionCode] ]
                csvwriter.writerow(entry) 
            csvfile.close()
            if self._DEBUG:
                print("  - csv file saved: "+self._csvKeyFilename)
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

    def getSessionKey(self,sessionCode):
        return self._dictionarySession.get(sessionCode)

    def getSessionCode(self,sessionKey):
        return self._dictionaryKey.get(sessionKey)

    # initialize the class
    # load the keys in dictionary if key file exist
    # or generate and save the key file otherwise
    def __init__(self, projectPath):
        if self._DEBUG:
            print("Session dictionary initialization: ")
        self._projectPath=projectPath
        self._txtKeyFilename = projectPath + "/key/sessionKeys.txt"
        self._csvKeyFilename = projectPath + "/key/sessionKeys.csv"
        self.__loadConfig()
        self.__cleanFiles()
        if not self.__load():
            self.__generate()
            self.__save()