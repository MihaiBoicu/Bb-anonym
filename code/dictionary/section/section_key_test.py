# Created by Mihai Boicu 
# python section/section_key_test.py

from dictionary.session import session_key
from dictionary.section import section_key

def main():
    sessionKey = session_key.SessionKey()
    sectionKey = section_key.SectionKey(sessionKey)

    testCodes = ["11233.202110", "10851.202110", "11067.202110", "11233.202140", "10851.202210", "11067.202170"]
    testKeys = []
    print("Testing the session dictionary with valid codes:")
    for code in testCodes:
        key = sectionKey.getSectionKey(code)
        print('Code '+str(code)+' has key '+str(key))
        testKeys.append(key)
    # print(testKeys)
    for key in testKeys:
        code = sectionKey.getSectionCode(key)
        print('Key '+str(key)+' has code '+str(code))
    # test invalid keys
    testKeys = [10000,10001,10002]
    for key in testKeys:
        code = sectionKey.getSectionCode(key)
        print('Key '+str(key)+' has code '+str(code))
    sectionKey.save()
