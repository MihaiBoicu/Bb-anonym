# Copyright Mihai Boicu 
import csv
import json
import os
import random
from dictionary.user import user_key
from dictionary.assignment import assignment_key
from dictionary.key import all_keys

class AllAttemptsExtract:

    _DEBUG : bool = False

    _allKeys : all_keys.AllKeys = None

    _format = None
    _regenerate = None
    _outputFilename = None
    _outputMultiplier : int
    _studentKeyMultiplier: int

    _result = []

    def __load(self):
        configFile = open(self._allKeys.configPath+"/attempt-extract.json", mode='r')
        configData = json.load(configFile)
        configFile.close()
        self._format = configData['format']
        self._regenerate = configData['regenerate']
        self._outputFilename = configData['output-filename'] 
        self._outputMultiplier = int(configData['output-multiplier']) 
        self._studentKeyMultiplier = int(configData['student-key-multiplier'])


    def __processAttemptsfile(self,filename):
        anonymData = []
        with open(self._allKeys.inboxPath+"/"+filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            rowNumber = 0
            for row in reader:
                rowNumber += 1
                if rowNumber == 1:
                    #process header
                    continue
                else:
                    #process data
                    assignmentName = row[8]
                    if self._allKeys.assignmentKey.isAnonymizedAssignment(assignmentName):
                        assignmentValue = float(row[3])
                        assignmentValues = self._allKeys.assignmentKey.getMultipleValues(assignmentName, assignmentValue, self._outputMultiplier)
                        lastName = row[0]
                        firstName = row[1]
                        userId = row[2]
                        userKeys = self._allKeys.userKey.getUserKeysFull(lastName,firstName, userId)
                        attempt = row[4]
                        assignmentOutputName = self._allKeys.assignmentKey.getAnonymizedName(assignmentName)
                        for i in range(0,self._outputMultiplier):
                            outRow = [userKeys[i], assignmentOutputName, attempt, assignmentValues[i]]
                            anonymData.append(outRow)
        return anonymData

    def __shuffle(self):
        last=len(self._result)-1
        for _ in range(0,last+1):
            i1=random.randint(0,last)
            i2=random.randint(0,last)
            temp = self._result[i1]
            self._result[i1] = self._result[i2]
            self._result[i2] = temp

    def __saveOutput(self):
        if self._format=="CSV":
            # writing to the csv file 
            filename = self._allKeys.outboxPath+"/"+self._outputFilename
            csvfile = open(filename, "w") 
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
            header = ["user","assignment","attempt","grade"]
            csvwriter.writerow(header)  
            # writing the fields 
            for dataRow in self._result:
                csvwriter.writerow(dataRow) 
            csvfile.close()
            return True   
        return False      

    def execute(self):
        print("Attempts Extract Project: "+self._allKeys.projectName)
        self._result = []
        for filename in os.listdir(self._allKeys.inboxPath):
            if filename.startswith("attempts_"):
                fileResult = self.__processAttemptsfile(filename)
                self._result.extend(fileResult)
        self.__shuffle()
        self.__saveOutput()

    def __init__(self, allKeys:all_keys.AllKeys):
        self._allKeys = allKeys
        self.__load()   
        self._allKeys.initUserKey(self._outputMultiplier)
        self._allKeys.initAssignmentKey()
