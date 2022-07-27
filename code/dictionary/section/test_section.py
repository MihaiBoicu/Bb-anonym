# Created by Mihai Boicu 
# python section/section_key_test.py

import json

from dictionary.key import all_keys
from dictionary.session import session_key
from dictionary.section import section_key


class TestSection:

    _DEBUG : bool = False

    _allKeys : all_keys.AllKeys = None

    _testCodes = None
    _invalidTestKeys = None

    def _load(self):
        configFile = open(self._allKeys.configPath+"/test-section.json", mode='r')
        configData = json.load(configFile)
        configFile.close()
        self._testCodes = configData['test-codes']
        self._invalidTestKeys = configData['invalid-test-keys']

    def execute(self):
        print("Test Section Project: "+self._allKeys.projectName)
        
        print("Testing the section dictionary with valid codes:")
        testKeys = []
        for code in self._testCodes:
            key = self._allKeys.sectionKey.getSectionKey(code)
            print('Code '+str(code)+' has key '+str(key))
            testKeys.append(key)
        for key in testKeys:
            code = self._allKeys.sectionKey.getSectionCode(key)
            print('Key '+str(key)+' has code '+str(code))    
        # test invalid codes
        print("Testing the section dictionary with invalid codes and keys:")
        for key in self._invalidTestKeys:
            code = self._allKeys.sectionKey.getSectionCode(key)
            print('Key '+str(key)+' has code '+str(code))
        self._allKeys.save()

    def __init__(self, allKeys:all_keys.AllKeys):
        self._allKeys = allKeys
        self._load()   
        self._allKeys.initSectionKey()
