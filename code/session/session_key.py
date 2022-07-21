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

    DEBUG = False

    # configuration file to be used to generate the keys
    CONFIG_FILE_NAME = "../../config/session-config.json"

    # key file with randomly generated keys for sessions
    # 
    KEY_FILE_NAME_TXT = "../../key/sessionKeys.txt"
    KEY_FILE_NAME_CSV = "../../key/sessionKeys.csv"

    # a map between a session (i.e. semester) and its anonymized code
    # example (200040, 198) will link Summer semester in 2000 with the code 198
    dictionarySession = {}
    dictionaryKey = {}
    dictionaryType = None

    # load the generated key file and initialize the dictionary
    # return true if succeeds, false otherwise
    def load(self):
        file = None
        if exists(self.KEY_FILE_NAME_TXT):
            file = open(self.KEY_FILE_NAME_TXT)
            lines = file.readlines()
            for line in lines:
                parts = line.split(" ")
                self.dictionarySession[int(parts[0])] = int(parts[1])
                self.dictionaryKey[int(parts[1])] = int(parts[0])
            file.close()
            if self.DEBUG:
                print("  - text file loaded: "+self.KEY_FILE_NAME_TXT)
            return True
        if exists(self.KEY_FILE_NAME_CSV):
            file = open(self.KEY_FILE_NAME_CSV, mode='r')
            csvFile = csv.reader(file)
            lineIndex = 0
            sessionCode = None
            sessionKey = None
            for lines in csvFile:
                for line in lines:
                    # if self.DEBUG:
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
                            self.dictionarySession[sessionCode] = sessionKey
                            self.dictionaryKey[sessionKey] = sessionCode
            if self.DEBUG:
                print("  - csv file loaded: "+self.KEY_FILE_NAME_CSV)
                print(self.dictionarySession)
                print(self.dictionaryKey)
            return True
        # otherwise no file
        print("  - dictionary file not found")
        return False
        
    # save the key file based on the current dictionary
    # return true if succeeds, false otherwise
    def save(self):
        if self.dictionaryType=="TXT":
            file = open(self.KEY_FILE_NAME_TXT, "w")
            for keyName in sorted(self.dictionary.keys()):
                file.write(str(keyName) + " " + str(self.dictionary[keyName]) + "\n")
            file.close()
            if self.DEBUG:
                print("  - text file saved: "+self.KEY_FILE_NAME_TXT)
            return True
        if self.dictionaryType=="CSV":
            # writing to the csv file 
            csvfile = open(self.KEY_FILE_NAME_TXT, "w") 
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
            header = [ "session", "key"]
            csvwriter.writerow(header)  
            # writing the fields 
            for keyName in sorted(self.dictionary.keys()):
                entry = [ keyName, self.dictionary[keyName] ]
                csvwriter.writerow(entry) 
            csvfile.close()
            if self.DEBUG:
                print("  - csv file saved: "+self.KEY_FILE_NAME_CSV)
            return True
        print("  - error saving dictionary")
        return False

    # generate a new dictionary (assumed empty)
    def generate(self):
        configFile = open(self.CONFIG_FILE_NAME, )
        configData = json.load(configFile)

        self.dictionaryType = configData['format']
        startYear = configData['start_year']
        endYear = configData['end_year']
        lastKey = configData['start_key']
        minStep = configData['min_step']
        maxStep = configData['max_step']
        semesters = configData['semesters_list']

        # for all years in the configuration range
        for i in range(startYear, endYear + 1):
            # for all the semesters
            for sem in semesters:
                # update the last key to a new valid key
                lastKey += random.randint(minStep, maxStep)
                # save the semester and key in dictionary
                self.dictionary[(i * 100 + sem)] = lastKey
        if self.DEBUG:
            print("  - random key dictionary generated")
        # debug info
        # print("lastKey: ",lastKey)
        # print("sessionDict: ", sessionDict)

    # initialize the class
    # load the keys in dictionary if key file exist
    # or generate and save the key file otherwise
    def __init__(self):
        if self.DEBUG:
            print("Session dictionary initialization: ")
        if not self.load():
            self.generate()
            self.save()

