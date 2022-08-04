# Author: Mihai Boicu

import csv
import json
import os
import random
import datetime

class Assignment:
    name: str
    grade: int
    durationSec: int
    outputName: str
    outputValue: str
    outputType: str
    outputRandom: float
    outputPrecision: float

    def anonimyzePercent(self, val):
        ov=val
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

    def getOutputDuration(self, duration):
        ov=self.computeSeconds(duration)
        if (self.outputValue=="percent100"):
            ov = 100*ov/self.durationSec
        return self.anonimyzePercent(ov)

    def getOutputValue(self,value):
        ov=value
        if (self.outputValue=="percent100"):
            ov = 100*ov/self.grade
        return self.anonimyzePercent(ov)

    def computeSeconds(self, duration:str):
        if duration=="open":
            return -1
        index1=duration.find(":")
        index2=duration.find(":",index1+1)
        hours = int(duration[0:index1])
        minutes = int(duration[index1+1:index2])
        seconds = int(duration[index2+1:])
        return hours*3600+60*minutes+seconds

    def __init__(self, assignmentJson):
        self.name = assignmentJson["name"]
        self.grade = assignmentJson["grade"]
        duration = assignmentJson["duration"]
        self.outputName = assignmentJson["output-name"]
        self.outputValue = assignmentJson["output-value"]
        self.outputType = assignmentJson["output-type"]
        self.outputRandom = float(assignmentJson["output-random"])
        self.outputPrecision = float(assignmentJson["output-precision"])
        self.durationSec = self.computeSeconds(duration)

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

    def getAnonymizedDuration(self, assignmentName, durationStr):
        a = self.__getAssignment(assignmentName)
        return a.getOutputDuration(durationStr)

    def getAnonymizedValue(self, assignmentName, valueStr):
        a = self.__getAssignment(assignmentName)
        val = float(valueStr)
        return a.getOutputValue(val)

    def getMultipleValues(self, name, value, multiplier):
        a = self.__getAssignment(name)
        result = []
        for i in range (0,multiplier):
            result.append(a.getOutputValue(value))
        return result

    def getAnonymizedSubmissionTime(self, assignName, subDateStr, dueDateStr):
        a=self.__getAssignment(assignName)
        subDate = None
        if subDateStr.endswith("LATE"):
            subDateStr = subDateStr[:-4]
            # February 9, 2022 4:39:30 PM
            subDate=datetime.datetime.strptime(subDateStr,'%B %d, %Y %I:%M:%S %p')
        else:
            # 2/6/22 23:59
            subDate=datetime.datetime.strptime(subDateStr,'%m/%d/%y %H:%M')
        dueDate = datetime.datetime.strptime(dueDateStr,'%m/%d/%y %H:%M')
        diff=dueDate-subDate
        diff=100.0*diff.total_seconds()/(7*24*60*60)
        if diff<-100:
            diff=-100
        return a.anonimyzePercent(diff)

    def getHeader(self):
        header = []
        for i in range(0,len(self._assignmentsList)):
            a:Assignment=self._assignmentsList[i]
            header.append(a.outputName)
        return header

    def getHeaderList(self, assignmentNames):
        header = []
        for an in assignmentNames:
            header.append(self.getAnonymizedName(an))
        return header

    def __init__(self, projectPath):
        self._projectPath=projectPath
        self.__loadConfig()