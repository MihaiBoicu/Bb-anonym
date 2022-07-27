# Copyright Mihai Boicu 

import json
from dictionary.key import all_keys
from dictionary.session import session_key

class TestSession:

    _DEBUG : bool = False

    _allKeys : all_keys.AllKeys = None

    _testCodes = None
    _invalidTestCodes = None
    _invalidTestKeys = None

    def _load(self):
        configFile = open(self._allKeys.configPath+"/test-session.json", mode='r')
        configData = json.load(configFile)
        configFile.close()
        self._testCodes = configData['test-codes']
        self._invalidTestCodes = configData['invalid-test-codes']
        self._invalidTestKeys = configData['invalid-test-keys']

    def execute(self):
        print("Test Session Project: "+self._allKeys.projectName)
        print("Testing the session dictionary with valid codes:")
        testKeys = []
        for code in self._testCodes:
            key = self._allKeys.sessionKey.getSessionKey(code)
            print('Code '+str(code)+' has key '+str(key))
            testKeys.append(key)
        for key in testKeys:
            code = self._allKeys.sessionKey.getSessionCode(key)
            print('Key '+str(key)+' has code '+str(code))    
        # test invalid codes
        print("Testing the session dictionary with invalid codes and keys:")
        for code in self._invalidTestCodes:
            key = self._allKeys.sessionKey.getSessionKey(code)
            print('Code '+str(code)+' has key '+str(key))
        # print(testKeys)
        for key in self._invalidTestKeys:
            code = self._allKeys.sessionKey.getSessionCode(key)
            print('Key '+str(key)+' has code '+str(code))

    def __init__(self, allKeys:all_keys.AllKeys):
        self._allKeys = allKeys
        self._load()    
        self._allKeys.initSessionKey()
