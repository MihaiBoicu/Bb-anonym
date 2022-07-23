# Author: Mihai Boicu
import json
from  dictionary.session import test_session

class Project:

    _DEBUG = False

    _name = None
    _directoryName = None
    _path = None
    _type = None

    def _load(self):
        configFile = open(self._path+"/config/project.json", mode='r')
        configData = json.load(configFile)
        configFile.close()
        self._name = configData['name']
        self._type = configData['type']

    def execute(self):
        if (self._type=="test-session"):
            t=test_session.TestSession(self._name,self._path)
            t.execute()
        else:
            print("Unknown type of project")

    def getName(self):
        return self._name

    def getPath(self):
        return self._path  

    def __init__(self, dirName, path):
        self._directoryName = dirName
        self._path = path
        self._load()