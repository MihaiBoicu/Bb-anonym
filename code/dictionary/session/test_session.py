# Copyright Mihai Boicu 

import json
from dictionary.session import session_key

class TestSession:

    _DEBUG : bool = False

    _projectName : str = None
    _projectPath : str = None

    _testCodes = None
    _invalidTestCodes = None
    _invalidTestKeys = None

    def _load(self):
        configFile = open(self._projectPath+"/config/test-session.json", mode='r')
        configData = json.load(configFile)
        configFile.close()
        self._testCodes = configData['test-codes']
        self._invalidTestCodes = configData['invalid-test-codes']
        self._invalidTestKeys = configData['invalid-test-keys']

    def execute(self):
        print("Test Session Project: "+self._projectName)
        sessionKey = session_key.SessionKey(self._projectPath) 
        print("Testing the session dictionary with valid codes:")
        testKeys = []
        for code in self._testCodes:
            key = sessionKey.getSessionKey(code)
            print('Code '+str(code)+' has key '+str(key))
            testKeys.append(key)
        for key in testKeys:
            code = sessionKey.getSessionCode(key)
            print('Key '+str(key)+' has code '+str(code))    
        # test invalid codes
        print("Testing the session dictionary with invalid codes and keys:")
        for code in self._invalidTestCodes:
            key = sessionKey.getSessionKey(code)
            print('Code '+str(code)+' has key '+str(key))
        # print(testKeys)
        for key in self._invalidTestKeys:
            code = sessionKey.getSessionCode(key)
            print('Key '+str(key)+' has code '+str(code))

    def __init__(self, projectName, projectPath):
        self._projectName = projectName
        self._projectPath = projectPath
        self._load()    
