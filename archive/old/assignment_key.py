import json

# Assignment Anonymization Key 

class AssignmentKey:
    configurationFileName = '../predefined-key/assignment-config.json'
    defaultTotalZeroPoints = 1

    dictionary = {}

    def load(self):
        configFile = open(self.configurationFileName,)
        configData = json.load(configFile)
        assignmentArray = configData['assignments']
        for group in assignmentArray:
            self.dictionary[group['name']] = group['code']
        configFile.close()

    def __init__(self):
        self.load()

    def getGC(self, gcName):
        pointsSplit = gcName.split("[")
        pointsPart = pointsSplit[1].split(' ')[2]
        points = 0.0
        if pointsPart == 'up':
            points = float(pointsSplit[1].split(' ')[4])
        else:
            points = float(pointsPart)      

        nameSplit = pointsSplit[0].split('-')[0].split('(')[0]
        name = str(nameSplit).strip()  # + ' [' + points + ']'
        if points == 0:
            points == self.defaultTotalZeroPoints
        if name in self.dictionary:
            return self.dictionary[name], points
        else:
            #print("Assignment name: " + anonAssiName + " not found within config file")
            #print("Defaulting assignment name.")
            return "IGNORE", points

    def getQR(self, qrName):
        print(qrName)
        name = qrName.strip()
        if name in self.dictionary:
            return self.dictionary[name]
        else:
            return "IGNORE"
