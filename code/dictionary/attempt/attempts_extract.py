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

    _assignments = []
    _columns = []
    _isStudentCol = False
    _isAssignmentCol = False
    _isAttemptCol = False
    _isGradeCol = False
    _isDurationCol = False
    _isSubmissionTimeCol = False

    _result = []

    def __printConfig(self):
        print("Attempts-extract configuration:")
        print("  - columns: "+str(self._columns))
        print("  - is student col: "+str(self._isStudentCol))
        print("  - is assignment col: "+str(self._isAssignmentCol))
        print("  - is attempt col: "+str(self._isAttemptCol))
        print("  - is grade col:  "+str(self._isGradeCol))
        print("  - is duration col:  "+str(self._isDurationCol))
        print("  - submission time col: "+str(self._isSubmissionTimeCol))
        

    def __load(self):
        configFile = open(self._allKeys.configPath+"/attempts-extract.json", mode='r')
        configData = json.load(configFile)
        configFile.close()
        self._format = configData['format']
        self._regenerate = configData['regenerate']
        self._outputFilename = configData['output-filename'] 
        self._columns = configData['columns']
        self._assignments = configData['assignments']
        for col in self._columns:
            if col=="student":
                self._isStudentCol=True
            elif col=="assignment":
                self._isAssignmentCol=True
            elif col=="attempt":
                self._isAttemptCol=True
            elif col=="grade":
                self._isGradeCol=True
            elif col=="duration":
                self._isDurationCol=True
            elif col=="submission-time":
                self._isSubmissionTimeCol=True
            else:
                print("Unexpected column name")
                exit(1)
        if self._DEBUG:
            self.__printConfig()

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
                    if assignmentName in self._assignments:
                        lastName = row[0]
                        firstName = row[1]
                        userId = row[2]
                        userKeys = self._allKeys.userKey.getUserKeysFull(lastName,firstName, userId)
                        assignmentGrade = row[3]
                        attempt = int(row[4])
                        date = row[5]
                        status = row[6]
                        duration = row[7]
                        course = row[9]
                        due = row[10]
                        assignmentOutputName = self._allKeys.assignmentKey.getAnonymizedName(assignmentName)
                        for student in userKeys:
                            outRow=[]
                            if self._isStudentCol:
                                outRow.append(student)
                            if self._isAssignmentCol:
                                outRow.append(assignmentOutputName)
                            if self._isAttemptCol:
                                outRow.append(attempt)
                            if self._isGradeCol:
                                outRow.append(self._allKeys.assignmentKey.getAnonymizedValue(assignmentName,assignmentGrade))
                            if self._isDurationCol:
                                outRow.append(self._allKeys.assignmentKey.getAnonymizedDuration(assignmentName, duration))
                            if self._isSubmissionTimeCol:
                                outRow.append(self._allKeys.assignmentKey.getAnonymizedSubmissionTime(assignmentName, date, due))
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
            header = []
            if self._isStudentCol:
                header.append("student")
            if self._isAssignmentCol:
                header.append("assignment")
            if self._isAttemptCol:
                header.append("attempt")
            if self._isGradeCol:
                header.append("grade")
            if self._isDurationCol:
                header.append("duration")
            if self._isSubmissionTimeCol:
                header.append("submission time")
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
        self._allKeys.initUserKey()
        self._allKeys.initAssignmentKey()
