# Created by Mihai Boicu 

# python user_key_test.py

import user_key;


def main():
    userKey = user_key.UserKey()
    print(userKey.get("jdoe1"))
    print(userKey.get("jdoe2"))
    print(userKey.get("jdoe1"))
    userKey.save()

if __name__ == '__main__':
    main()