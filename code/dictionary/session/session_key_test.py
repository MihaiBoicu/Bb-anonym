# Mihai Boicu 

from dictionary.session import session_key;

def main():
    sessionKey = session_key.SessionKey()
    testCodes = [202010, 202040, 202070, 202110, 202140, 202170]
    testKeys = []
    print("Testing the session dictionary with valid codes:")
    for code in testCodes:
        key = sessionKey.getSessionKey(code)
        print('Code '+str(code)+' has key '+str(key))
        testKeys.append(key)
    # print(testKeys)
    for key in testKeys:
        code = sessionKey.getSessionCode(key)
        print('Key '+str(key)+' has code '+str(code))
    # test invalid codes
    testCodes = [205010, 205040]
    print("Testing the session dictionary with invalid codes:")
    for code in testCodes:
        key = sessionKey.getSessionKey(code)
        print('Code '+str(code)+' has key '+str(key))
    # print(testKeys)
    testKeys = [10000,10001,10002]
    for key in testKeys:
        code = sessionKey.getSessionCode(key)
        print('Key '+str(key)+' has code '+str(code))


