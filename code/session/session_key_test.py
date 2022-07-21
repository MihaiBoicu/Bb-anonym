# Created by Mihai Boicu 

# python session_key_test.py

import session_key;

def main():
    sessionKey = session_key.SessionKey()
    testCodes = [202010, 202040, 202070, 202110, 202140, 202170]
    testKeys = []
    print("Testing the session dictionary:")
    for code in testCodes:
        key = sessionKey.dictionarySession[code]
        print('Code '+str(code)+' has key '+str(key))
        testKeys.append(key)
    # print(testKeys)
    for key in testKeys:
        key = sessionKey.dictionarySession[code]
        print('Key '+str(key)+' has code '+str(code))

if __name__ == '__main__':
    main()

