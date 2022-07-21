# Anonymizing the Course Sections

Contributers:
- Mouhamed Sylla (Documentation) Spring 2022

Editor and reviewer:
- Mihai Boicu

## Understanding how to configure the class section key

The class section is used to randomize the section code (i.e. 10851.202110) of a GMU course. This code will be randomized using the sesession anonymized key for the session part (e.g., 395 for 202110), and will generate a random number from 0 to a max value for the section code (i.e. 10851). 

The final code will be obtained by the formula:
- sesessioncode * maxvalue + section code

Based on the number of section that you plan to anonymize in each session, you may change the max value in the code (i.e., MAX_SECTIONS_PER_SESSION). Its default value is 100.

This section code appears in the name of the files when downloaded from the Blackboard, or must be added to the name of some files. For instance a grade book downloaded file will contain the section code in its name.

## Sample of output in section_key

```
10851.202110 290336
11067.202110 290357
11233.202110 290319
```

These numbers were generated using the code:

```
def main():
	    sessionKey = session_key.SessionKey()
	    sectionKey = section_key.SectionKey(sessionKey)
	    print(sectionKey.get("11233.202110"))
	    print(sectionKey.get("10851.202110"))
	    print(sectionKey.get("11067.202110"))
	    sectionKey.save()
```

and formula of:
- sesessioncode * maxvalue + section code

for the sessioncode corresponding to 202110 being 2903 and the maxvalue being 100.

For example "11233.202110" is associated with 290319:
- 2903 is the code for the session 202110 (already generated and saved in the session key)
- the maxvalue is 100
- the section code is a generated random number less than 100, in this case 19.
- using the formula we obtain, 2903*100+19 = 290319
- the Output is then put into the sectionkey.txt file when save is called and will be used for this section from now on

## Understanding how to call the class section key
\
To use the anonymized section key you must:
- import the session key 
```
import session_key
```
- create a unique session key instance (only one must be created and used in all the code)
```
  sessionKey = session_key.SessionKey()
```
- import the section key code
```
import section_key;
```
- create only one instance of the SectionKey class (do not duplicate the instance in all your code)
```
  sectionKey = section_key.SectionKey(sessionKey)
```
- always this class will be used in tandem with the session key file and you must create only one instance of each for your entire code
- to get the key for a given section you must call get method; if a section code already exists is returned, if not, a new code is generated and returned; 
```
  sectionKey.get("11233.202110")
```
- the new sections codes created are not automatically saved in your key file; you must call save when you finish the anonymization
```
  sectionKey.save()
```

## Understanding how the class section key is coded

The following imports are used by SectionKey:
```
import os
import random
import session_key
```

The class SectionKey is using the class SessionKey (file section_key.py). You must first  initialize the session key and use this instance in your section initialization. First time when is used the SessionKey instance will generate and same the anonymization codes for each session, and in further calls the same will be reused. 

By default, there are maximum 100 sections per session. This is hardcoded in the coode/section_key.py. You can modify it before you start the anonymization process.
```
    # maximum number of sections allowed in a session
    MAX_SECTIONS_PER_SESSION = 100
```
By default, the anonymization key is stored in the file key/sectionKeys.txt. If you want to change the key file you must modify the value of the following constant:
```
    # key file with randomly generated keys for sections
    KEY_FILE_NAME = "../key/sectionKeys.txt"
```
==== CONTINUE FROM HERE

This is where the keys are held after being saved and generated. 
Section_key_test.py can be used to run a moch test to generate numbers. Like the moch test Section uses import session_key and import section_key.
```
 def load(self):
        file = open(self.keyFileName, "r")
        lines = file.readlines()
        for line in lines:
            sections = line.split(" ")
            self.dictionary[str(sections[0])] = sections[1]
        file.close()
```
Uses the file open to retrieve the numbers that have been generated and read. Next opens file, writes in file, and sorts values.
```
   parts = section.split(".")
        sectionPart = int(parts[0])
        sessionPart = int(parts[1])
        sessionCode = self.sessionKey.dictionary[sessionPart]
        sectionCode = -1
```
After getting the numbers we use split to differentiate the section and time to make the numbers clear but randomized in a specific order
```

        while True:
            sectionCode = int(sessionCode * 100 + random.random() * 100)
            if not sectionCode in self.dictionary.values():
                break
        self.dictionary[section] = sectionCode
        # return code
        return self.dictionary[section]
```
Needs to use a formula to make sure there is actual randomization so the while loop is choosen to output the formula.


## Understand how to call the Section Key 
```
Import section_key.py
,
sectionKey = SectionKey(sessionKey)
```


