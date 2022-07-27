# Copyright Mihai Boicu 
import csv
import json
import os
import random
from dictionary.assignment import assignment_key
from dictionary.key import all_keys

class GradeCenterExtract:

    _DEBUG : bool = False

    _allKeys : all_keys.AllKeys = None

    _format = None
    _regenerate = None
    _outputFilename = None
    _columns = []

    _studentCol = False
    _assignments = []
    _result = []

    def __load(self):
        configFile = open(self._allKeys.projectPath+"/config/gc-extract.json", mode='r')
        configData = json.load(configFile)
        configFile.close()
        self._format = configData['format']
        self._regenerate = configData['regenerate']
        self._outputFilename = configData['output-filename'] 
        self._columns = configData['columns']
        self._assignments = [] 
        for col in self._columns:
            if col=="student":
                self._studentCol=True
            else:
                self._assignments.append(col)

    def __gcColumnName(self,fullName:str):
        totalIndex = fullName.find("[")
        if totalIndex>0:
            fullName=fullName[:totalIndex]
        return fullName.strip()

    def __getIndexList(self, assignmentsNames):
        indexList = []
        for a in self._assignments:
            index = None
            for i in range(0,len(assignmentsNames)):
                if a == assignmentsNames[i]:
                    index=i
                    break
            indexList.append(index)
        return indexList

    def __processGCfile(self,filename):
        anonymData = []
        with open(self._allKeys.inboxPath+"/"+filename, newline='') as csvfile:
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
                    extractIndexes = self.__getIndexList(allColumns)
                else:
                    #process data
                    extractData=[]
                    for i in extractIndexes:
                        extractData.append(row[i])
                    studentLastName=row[0]
                    studentFirstName=row[1]
                    studentCode=row[2]
                    studentKeys=self._allKeys.userKey.getUserKeysFull(studentLastName, studentFirstName, studentCode)
                    for i in range(0,len(studentKeys)):
                        anonymRow=[]
                        if self._studentCol:
                            anonymRow.append(studentKeys[i])
                        for c in range(0,len(extractData)):
                            val=self._allKeys.assignmentKey.getAnonymizedValue(self._assignments[c], extractData[c])
                            anonymRow.append(val)
                        if self._DEBUG:
                            print(str(anonymRow))
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
            filename = self._allKeys.outboxPath+"/"+self._outputFilename
            csvfile = open(filename, "w") 
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
            header = []
            if self._studentCol:
                header.append("student")
            header.extend(self._allKeys.assignmentKey.getHeaderList(self._assignments))
            csvwriter.writerow(header)  
            # writing the fields 
            for dataRow in self._result:
                csvwriter.writerow(dataRow) 
            csvfile.close()
            return True   
        return False      

    def execute(self):
        print("GC Extract Project: "+self._allKeys.projectName)
        self._result = []
        for filename in os.listdir(self._allKeys.inboxPath):
            if filename.startswith("gc_"):
                fileResult = self.__processGCfile(filename)
                self._result.extend(fileResult)
        self.__shuffle()
        if self._DEBUG:
            print(str(self._result))
        self.__saveOutput()
        

    def __init__(self, allKeys:all_keys.AllKeys):
        self._allKeys = allKeys
        self.__load()   
        self._allKeys.initAssignmentKey()
        self._allKeys.initUserKey()
