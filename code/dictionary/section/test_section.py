# Created by Mihai Boicu 
# python section/section_key_test.py

import json

from dictionary.session import session_key
from dictionary.section import section_key


class TestSection:

    _DEBUG : bool = False

    _projectName : str = None
    _projectPath : str = None
    _sessionKey = None
    _sectionKey = None

    _testCodes = None
    _invalidTestKeys = None

    def _load(self):
        configFile = open(self._projectPath+"/config/test-section.json", mode='r')
        configData = json.load(configFile)
        configFile.close()
        self._testCodes = configData['test-codes']
        self._invalidTestKeys = configData['invalid-test-keys']

    def execute(self):
        print("Test Section Project: "+self._projectName)
        self._sessionKey = session_key.SessionKey(self._projectPath) 
        self._sectionKey = section_key.SectionKey(self._projectPath, self._sessionKey)
        print("Testing the section dictionary with valid codes:")
        testKeys = []
        for code in self._testCodes:
            key = self._sectionKey.getSectionKey(code)
            print('Code '+str(code)+' has key '+str(key))
            testKeys.append(key)
        for key in testKeys:
            code = self._sectionKey.getSectionCode(key)
            print('Key '+str(key)+' has code '+str(code))    
        # test invalid codes
        print("Testing the section dictionary with invalid codes and keys:")
        for key in self._invalidTestKeys:
            code = self._sectionKey.getSectionCode(key)
            print('Key '+str(key)+' has code '+str(code))
        self._sectionKey.save()

    def __init__(self, projectName, projectPath):
        self._projectName = projectName
        self._projectPath = projectPath
        self._load()   
