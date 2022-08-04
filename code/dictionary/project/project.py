# Author: Mihai Boicu
import json
import os.path
from dictionary.gradecenter import gc_extract
from dictionary.attempt import attempts_extract
from dictionary.session import test_session
from dictionary.section import test_section
from dictionary.key import all_keys

class Project:

    _DEBUG : bool = False

    _type : str = None
    _types = []

    _allKeys : all_keys.AllKeys = None

    def __printConfig(self, configData):
        print("Project: Config information")
        print("  - config data: "+str(configData))
        print("  - type: "+str(self._type))
        print("  - types: "+str(self._types))

    def __load(self):
        configFile = open(self._allKeys.configPath+"/project.json", mode='r')
        configData = json.load(configFile)
        configFile.close()
        name = configData['name']
        self._type = configData['type']
        if self._type=='combined':
            self._types = configData['types']
        self._allKeys.setName(name)
        if self._DEBUG:
            self.__printConfig(configData)

    def __executeType(self, type):
        if type=="gc-extract":
            t=gc_extract.GradeCenterExtract(self._allKeys)
            t.execute()
        elif type=="attempts-extract":
            t= attempts_extract.AllAttemptsExtract(self._allKeys)
            t.execute()
        elif type=="test-session":
            t=test_session.TestSession(self._allKeys)
            t.execute()
        elif type=="test-section":
            t=test_section.TestSection(self._allKeys)
            t.execute()                 
        else:
            print("Unknown type of project")

    def execute(self):
        if self._type=="combined":
            for type in self._types:
                self.__executeType(type)
        else: 
            self.__executeType(self._type)
        self._allKeys.save()

    def getName(self):
        return self._allKeys.projectName

    def getPath(self):
        return self._allKeys.projectPath  

    def __init__(self, dirName, path):
        if self._DEBUG:
            print("Debug project.py")
            print("  - dirName="+dirName)
            print("  - path="+path)
        self._allKeys = all_keys.AllKeys(dirName, path)
        self.__load()
        