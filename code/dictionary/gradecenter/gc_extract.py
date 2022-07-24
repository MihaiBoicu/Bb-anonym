# Copyright Mihai Boicu 
import csv
import json
import os
import random
from dictionary.assignment import assignment_key

class GradeCenterExtract:

    _DEBUG : bool = False

    _projectName : str = None
    _projectPath : str = None

    _assignmentKey : assignment_key.AssignmentKey = None

    _format = None
    _regenerate = None
    _outputFilename = None
    _outputMultiplier : int

    _inboxFolder = None

    _result = []

    def __load(self):
        configFile = open(self._projectPath+"/config/gc-extract.json", mode='r')
        configData = json.load(configFile)
        configFile.close()
        self._format = configData['format']
        self._regenerate = configData['regenerate']
        self._outputFilename = configData['output-filename'] 
        self._outputMultiplier = int(configData['output-multiplier']) 

    def __gcColumnName(self,fullName:str):
        totalIndex = fullName.find("[")
        if totalIndex>0:
            fullName=fullName[:totalIndex]
        return fullName.strip()

    def __processGCfile(self,filename):
        anonymData = []
        with open(self._inboxFolder+"/"+filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            rowNumber = 0
            extractIndexes=[]
            for row in reader:
                rowNumber += 1
                if rowNumber == 1:
                    #process header
                    allColumns=[]
                    for columnIndex in range(0, len(row)):
                        columnName = self.__gcColumnName(row[columnIndex])
                        allColumns.append(columnName)
                    extractIndexes = self._assignmentKey.getIndexList(allColumns)
                else:
                    #process data
                    extractData=[]
                    for i in extractIndexes:
                        extractData.append(row[i])
                    for i in range(0,self._outputMultiplier):
                        anonymRow = self._assignmentKey.getAnonymizedValues(extractData)
                        anonymData.append(anonymRow)
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
            filename = self._projectPath+"/outbox/"+self._outputFilename
            csvfile = open(filename, "w") 
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
            header = self._assignmentKey.getHeader()
            csvwriter.writerow(header)  
            # writing the fields 
            for dataRow in self._result:
                csvwriter.writerow(dataRow) 
            csvfile.close()
            return True   
        return False      

    def execute(self):
        print("GC Extract Project: "+self._projectName)
        self._result = []
        for filename in os.listdir(self._inboxFolder):
            if filename.startswith("gc_"):
                fileResult = self.__processGCfile(filename)
                self._result.extend(fileResult)
        self.__shuffle()
        self.__saveOutput()

    def __init__(self, projectName, projectPath):
        self._projectName = projectName
        self._projectPath = projectPath
        self.__load()   
        self._inboxFolder = projectPath + "/inbox"
        self._assignmentKey = assignment_key.AssignmentKey(projectPath)