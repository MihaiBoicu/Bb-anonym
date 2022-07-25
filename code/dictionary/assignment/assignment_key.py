# Author: Mihai Boicu

import csv
import json
import os
import random

class Assignment:
    name: str
    grade: int
    outputName: str
    outputValue: str
    outputType: str
    outputRandom: float
    outputPrecision: float

    def getOutputValue(self,value):
        ov=value
        if (self.outputValue=="percent100"):
            ov = 100*ov/self.grade
        if self.outputRandom!=0:
            if ov>15:
                ov = ov - self.outputRandom + 2 * self.outputRandom * random.random()
            else:
                ov = ov + self.outputRandom * random.random()
        ov = int(ov / self.outputPrecision)
        ov = 1.0 * ov * self.outputPrecision
        if (self.outputType=="int"):
            return int(round(ov,0))
        return ov

    def __init__(self, assignmentJson):
        self.name = assignmentJson["name"]
        self.grade = assignmentJson["grade"]
        self.outputName = assignmentJson["output-name"]
        self.outputValue = assignmentJson["output-value"]
        self.outputType = assignmentJson["output-type"]
        self.outputRandom = float(assignmentJson["output-random"])
        self.outputPrecision = float(assignmentJson["output-precision"])

class AssignmentKey:

    _DEBUG = False
    
    _projectPath = None

    _assignmentsList = []

    def __loadConfig(self):
        configFile = open(self._projectPath+"/config/assignment.json", mode='r')
        configData = json.load(configFile)
        configFile.close()
        assignments = configData['assignments']
        for a in assignments:
            assignment = Assignment(a)
            self._assignmentsList.append(assignment)

    def getIndexList(self, assignmentsNames):
        indexList = []
        for a in self._assignmentsList:
            index = None
            processedAssignment:Assignment=a
            for i in range(0,len(assignmentsNames)):
                if processedAssignment.name == assignmentsNames[i]:
                    index=i
                    break
            indexList.append(index)
        return indexList

    def isAnonymizedAssignment(self, assignmentName): 
        for i in range(0,len(self._assignmentsList)):
            a:Assignment=self._assignmentsList[i]
            if a.name==assignmentName:
                return True
        return False

    def __getAssignment(self, assignmentName):
        for i in range(0,len(self._assignmentsList)):
            a:Assignment=self._assignmentsList[i]
            if a.name==assignmentName:
                return a
        return None          

    def getAnonymizedName(self, assignmentName):
        for i in range(0,len(self._assignmentsList)):
            a:Assignment=self._assignmentsList[i]
            if a.name==assignmentName:
                return a.outputName
        return None            

    def getAnonymizedValues(self, data):
        result = []
        for i in range(0,len(self._assignmentsList)):
            a:Assignment=self._assignmentsList[i]
            vstr=data[i]
            v=None
            try:
                v=float(vstr)
            except ValueError:
                v=None
            if v!=None:
                v=a.getOutputValue(v)
            result.append(v)
        return result



    def getMultipleValues(self, name, value, multiplier):
        a = self.__getAssignment(name)
        result = []
        for i in range (0,multiplier):
            result.append(a.getOutputValue(value))
        return result

    def getHeader(self):
        header = []
        for i in range(0,len(self._assignmentsList)):
            a:Assignment=self._assignmentsList[i]
            header.append(a.outputName)
        return header

    def __init__(self, projectPath):
        self._projectPath=projectPath
        self.__loadConfig()