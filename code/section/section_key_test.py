# Created by Mihai Boicu 

import session_key
import section_key

def main():
    sessionKey = session_key.SessionKey()
    sectionKey = section_key.SectionKey(sessionKey)
    print(sectionKey.get("11233.202110"))
    print(sectionKey.get("10851.202110"))
    print(sectionKey.get("11067.202110"))
    sectionKey.save()

if __name__ == '__main__':
    main()