
from dictionary.user import user_key;

def main():
    userKey = user_key.UserKey()
    testFull = [["Doe","John","jdoe"], ["Doe","Jane","jdoe1"], ["Smith","Mark","msmith"]]
    testKeys = []
    print("Testing the user dictionary with valid full codes:")
    for code in testFull:
        key = userKey.getUserKeyFull(code[0], code[1], code[2])
        print('Code '+str(code[2])+' has key '+str(key))
        testKeys.append(key)
    # print(testKeys)
    for key in testKeys:
        code = userKey.getUserCode(key)
        print('Key '+str(key)+' has code '+str(code))
    # test invalid codes
    testCodes = ["jj", "aa"]
    print("Testing the session dictionary with invalid codes:")
    for code in testCodes:
        key = userKey.getUserKey(code)
        print('Code '+str(code)+' has key '+str(key))
    # print(testKeys)
    testKeys = [10000,10001,10002]
    for key in testKeys:
        code = userKey.getUserCode(key)
        print('Key '+str(key)+' has code '+str(code))
    userKey.save()