import os
import shutil
from datetime import date
import csv
import anonym_key


# Anonymization Process Class

class AnonymProcess:
    inboxFolder = '../inbox/'
    outboxFolder = '../outbox/'
    archiveFolder = '../archive/'

    key = anonym_key.AnonymKey()

    inboxFiles = []

    def initInboxFiles(self):
        try:
            self.inboxFiles = os.listdir(self.inboxFolder)
        except FileNotFoundError:
            exit("You do not have an inbox folder!")

    def initOutboxFolder(self):
        try:
            os.listdir(self.outboxFolder)
        except FileNotFoundError:
            exit("You do not have an outbox folder!")

    def __init__(self):
        self.initInboxFiles()
        self.initOutboxFolder()

    def printInboxFiles(self):
        print("*****")
        print("INBOX files:")
        for entry in self.inboxFiles:
            print(entry)
    
    def print(self):
        self.key.print()
        self.printInboxFiles()
    
    def gcProcessFileName(self, fileName):
        outputName = "gc_"
        inputArray = fileName.split("_")
        if len(inputArray) != 4:
            exit("Unexpected file name"+fileName)
        # section
        outputName += str(self.key.sectionKey.get(inputArray[1]))
        # type 
        outputName += "_" + inputArray[2] + "_"
        # date-time
        dateArray = inputArray[3].split("-")
        # 2021-06-24-09-37-32
        # 0    1  2  3  4  5
        stringName = str(fileName)
        yearName = stringName[9:13]
        sectionY = int(yearName)
        fileY = int(int(dateArray[0]))
        dayDiff = 400
        if fileY == sectionY:
            term=str(inputArray[1])[11]
            month=1
            if term=="1":
                month=1
            elif term=="4":
                month=5
            elif term=="7":
                month=8
            f_date = date(fileY, month, 15)
            l_date = date(int(dateArray[0]), int(dateArray[1]), int(dateArray[2]))
            delta = l_date - f_date
            dayDiff = delta.days + 1
        outputName += str(dayDiff) + "-" + dateArray[3] + "-" + dateArray[4] + ".csv"
        return outputName
    
    def gcProcess(self,inputFile, format):
        inputFileName=str(inputFile)
        outputFileName=self.gcProcessFileName(inputFileName)
        print("Process GC file: "+str(inputFileName))
        print("Output GC file: "+str(outputFileName))
 
        inboxFile = self.inboxFolder+inputFileName
        outboxFile = self.outboxFolder + str(outputFileName)
        archiveFile = self.archiveFolder + inputFileName

        data = []
        points = []
        counter = 0
        ffiledate = date(2021, 6, 1)
        with open(inboxFile, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # print("DEBUG: row[0]="+row[0])
                # print("DEBUG: row[1]="+row[1])
                data.append([])
                if counter == 0:
                    for columnIndex in range(0, len(row)):
                        if columnIndex >= 6:
                            assignmentName, assignmentPoints = self.key.assignmentKey.getGC(row[columnIndex])
                            points.append(assignmentPoints)
                            data[counter].append(assignmentName)
                        elif columnIndex < 2 or columnIndex == 5 or columnIndex == 3 or columnIndex == 4:
                            pass
                        else:
                            data[counter].append(row[columnIndex])
                else:
                    data[counter].append(self.key.userKey.get(row[2]))
                    # print("DEBUG: row[4]="+row[4])
                    # rowDate = row[4]
                    # lfiledate = date(int(rowDate[0:4]), int(rowDate[5:7]), int(rowDate[8:10]))
                    # delta = lfiledate - ffiledate
                    # dayDiff = delta.days + 1
                    # data[counter].append(str(dayDiff))

                    for columnIndex in range(6, len(row)):
                        try: 
                            val = float(row[columnIndex])
                            if format=="percent":
                                val = val/points[columnIndex-6]
                            data[counter].append(val)                            
                        except:
                            data[counter].append("")

                counter += 1

        with open(outboxFile, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in data:
                writer.writerow(row)

        shutil.move(inboxFile, archiveFile)   

    def qrProcessFileName(self, fileName):
        outputName = "qr_"
        inputArray = fileName.split("_")
        # section
        outputName += str(self.key.sectionKey.get(inputArray[1]))
        # type
        inputArray2 = inputArray[2].split("-")
        assiname = inputArray2[0]
        assiname = (self.key.assignmentKey.getQR(assiname))
        outputName += "_" + assiname + ".csv"
        return outputName

    def qrProcessData(self, fileName):
        data = []  # this data array will be used to store the data in the csv file
        counter = 0  # counter for the algorithm, will act as the row counter
        with open(fileName, newline='') as csvfile:  # grabs the file that exists at original, opens it
            reader = csv.reader(csvfile)  # reader scans through original file
            for row in reader:  # loops through every row in reader (row is an array of the columns for the row)
                data.append([])  # data appends another array, making it a 2d array
                if counter == 0:  # if this is the first row (column headers)
                    for columnIndex in range(0, len(row)):  # loops through every index for the row
                        # if columnIndex >= 6:  # if the columnn index is more than 6, this is an assignment name
                        # data[counter].append(anonAssignment(row[columnIndex]))  # calls the anonAssignment method to anonymize the name
                        # appends it to the 2d array of the current row (counter)
                        if columnIndex <= 2 or columnIndex == 4 or columnIndex == 7:  # These columns need to be deleted (first name, last name, ...)
                            pass  # pass so it never gets added to the data 2d array
                        else:
                            columnName = row[columnIndex]
                            if (columnName == "Question ID"):
                                columnName = "User ID"
                            if (columnName == "Manual Score"):
                                columnName = "Points Received"
                            data[counter].append(columnName)  # this means it is a columnn that can stay unchanged
                else:  # if this is not the first row (actual data of the students)
                # print(row)
                    data[counter].append(self.key.userKey.get(row[2]))

                    for columnIndex in range(5, len(row) - 1):
                        rowinp = row[columnIndex]  # appends the student data from column 6 and on (student scores)
                        if (columnIndex == 5 and (rowinp.lower() == "right" or rowinp.lower() == "wrong")):
                            rowinp = "TF"
                        elif (columnIndex == 5 and (rowinp.find("__") != 1)):
                            rowinp = "FITB"
                        data[counter].append(rowinp)
                        # appends the data to the 2d array
                counter += 1  # increments counter, signifying to go to the next row, stepping the 2d array when it is called
        return data

    def qrProcess(self,inputFile):
        inputFileName=str(inputFile)
        outputFileName=self.qrProcessFileName(inputFileName)
        print("Process QR file: "+str(inputFileName))
        print("Output QR file: "+str(outputFileName))
        original = r'../inbox/' + str(inputFile)
        target = r'../outbox/' + outputFileName
        archive = r'../archive/' + str(inputFile)
        data = self.qrProcessData(original)
        with open(target, 'w', newline='') as csvfile:  # creates a new csv file at target path
            writer = csv.writer(csvfile)  # writer starts writing into file
            for row in data:
                if row:# for every row in the 2d array data (row is an array here)
                    writer.writerow(row)  # writes row, the 1d array, into the file
        shutil.move(original, archive) 

    
    def aaProcessFileName(self, fileName):
        outputName = "aa_"
        inputArray = fileName.split("_")
        # section
        outputName += str(self.key.sectionKey.get(inputArray[1]))
        # type
        assiname = inputArray[2]
        assiname = assiname.split("-")[0]
        assiname = (self.key.assignmentKey.getQR(assiname))
        outputName += "_" + assiname + ".csv"
        return outputName

    def aaProcessData(self, fileName):
        data = []  # this data array will be used to store the data in the csv file
        counter = 0  # counter for the algorithm, will act as the row counter
        with open(fileName, newline='') as csvfile:  # grabs the file that exists at original, opens it
            reader = csv.reader(csvfile)  # reader scans through original file
            for row in reader:  # loops through every row in reader (row is an array of the columns for the row)
                data.append([])  # data appends another array, making it a 2d array
                if counter == 0:  # if this is the first row (column headers)
                    data[counter].append("User ID")
                    data[counter].append("Grade")
                    data[counter].append("Attempt")
                    data[counter].append("Duration")
                else:  # if this is not the first row (actual data of the students)
                # print(row)
                    data[counter].append(self.key.userKey.get(row[2]))
                    data[counter].append(row[3])
                    data[counter].append(row[4])
                    data[counter].append(row[7])
                counter += 1  # increments counter, signifying to go to the next row, stepping the 2d array when it is called
        return data

    def aaProcess(self,inputFile):
        inputFileName=str(inputFile)
        outputFileName=self.aaProcessFileName(inputFileName)
        print("Process AA file: "+str(inputFileName))
        print("Output AA file: "+str(outputFileName))
 
        original = r'../inbox/' + str(inputFile)
        target = r'../outbox/' + outputFileName
        archive = r'../archive/' + str(inputFile)
        data = self.aaProcessData(original)
        with open(target, 'w', newline='') as csvfile:  # creates a new csv file at target path
            writer = csv.writer(csvfile)  # writer starts writing into file
            for row in data:
                if row:# for every row in the 2d array data (row is an array here)
                    writer.writerow(row)  # writes row, the 1d array, into the file
        shutil.move(original, archive) 

    # format: "points" or "percent"
    def run(self, format):
        for inFile in self.inboxFiles:
            inFileName = str(inFile)
            if inFileName == "-1":  # th
                break
            if inFileName.startswith("gc_"):
                self.gcProcess(inFile, format)
            elif inFileName.startswith("qr_"):
                self.qrProcess(inFile)
            elif inFileName.startswith("aa_"):
                self.aaProcess(inFile)
            elif not inFileName.startswith("."):
                print("Unknown type of file: "+inFileName)
        self.key.save()
