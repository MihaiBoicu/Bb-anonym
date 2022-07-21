# Maintained by Mihai Boicu based on code created by:
# 2021 July-August
# - David Liu (a1.py, a2.py gc processing)
# - Anish Malik (a3.py - qr processing)
# 2022 March-April
# - Mouhamed Syllas (extract code and comment)
# - Mihai Boicu (update code/comments for clarity)

import os
import random
import session_key

# Anonymization of the Section Key
class SectionKey:

    # key file with randomly generated keys for sections
    KEY_FILE_NAME = "../key/sectionKeys.txt"

    # maximum number of sections allowed in a session
    MAX_SECTIONS_PER_SESSION = 100

    # the session anonymization key
    sessionKey: session_key.SessionKey

    # a map between a section code in a given semester and its anonymized code
    # example "11233.202110" is associated with 12345 where 123 is the code for session 202110 and 45 is the code for section 11233
    dictionary = {}

    # load the current anonymization file and initialize the dictionary
    def load(self):
        file = open(self.KEY_FILE_NAME, "r")
        lines = file.readlines()
        for line in lines:
            parts = line.split(" ")
            self.dictionary[str(parts[0])] = parts[1]
        file.close()

    # save the current dictionary in the key file 
    def save(self):
        file = open(self.KEY_FILE_NAME, "w")
        for keyName in sorted(self.dictionary.keys()):
            file.write(str(keyName) + " " + str(self.dictionary[keyName]) + "\n")
        file.close()

    # return the existing key for the given section, if any 
    # or create and return a new key
    def get(self, section):

        # return current key if section already defined in dictionary
        if section in self.dictionary.keys():
            return self.dictionary[section]

        # define new code
        # identify the session in section name
        # i.e.  202110 in "11233.202110"
        parts = section.split(".")
        sessionPart = int(parts[1])
        sessionCode = self.sessionKey.dictionary[sessionPart]
        sectionCode = -1

        # randomly generate a new (not used) anonymized value for the section grouping the sections in the same session together
        while True:
            sectionCode = int(sessionCode * self.MAX_SECTIONS_PER_SESSION + random.random() * self.MAX_SECTIONS_PER_SESSION)
            if not sectionCode in self.dictionary.values():
                break
        # save the value in the dictionary
        self.dictionary[section] = sectionCode
        # return the generated code
        return self.dictionary[section]

    # Initialize the section key based on the saved key file, if any
    def __init__(self, sessionKey):
        self.sessionKey=sessionKey
        if os.path.isfile(self.KEY_FILE_NAME):
            self.load()


# REVISE
#This section of the code is nessecary for this research because the section of the class in question has to be randomized
#If the section is not randomized it is easy to tell which student is from which because the section divides students up by classes.
#Firstly needs to access the data and seperate the different sections by making them strings and giving value numbers to hold them such as
#sections[1] and close. Next save the file and loads seesion key file and uses isfile to make sure the keyfile exist
#After making sure the file exist the code moves onto loading and once loaded randomizing the section uses while loop
#to keep randomizing sections untill there is a section number that does not exist in the dictionary. The equation is
#(sessionCode * 100 + random.random() * 100)