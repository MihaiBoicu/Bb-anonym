# Author: Mihai Boicu
import json
import os.path
from dictionary.gradecenter import gc_extract
from dictionary.session import test_session
from dictionary.section import test_section

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

    def _initFolder(self,folderName):
        folderPath = self._path+"/"+folderName
        if not os.path.exists(folderPath):
            os.mkdir(folderPath)

    def _initFolders(self):
        self._initFolder("inbox")
        self._initFolder("key")
        self._initFolder("outbox")

    def execute(self):
        if self._type=="gc-extract":
            t=gc_extract.GradeCenterExtract(self._name,self._path)
            t.execute()
        elif self._type=="test-session":
            t=test_session.TestSession(self._name,self._path)
            t.execute()
        elif self._type=="test-section":
            t=test_section.TestSection(self._name,self._path)
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
        self._initFolders()