import os
import random
import session_key
import assignment_key
import user_key
import section_key


# New object is created for session key, assignment key, user key and section key
class AnonymKey:
    sessionKey = session_key.SessionKey()
    assignmentKey = assignment_key.AssignmentKey()
    userKey = user_key.UserKey()
    sectionKey = section_key.SectionKey(sessionKey)

    # It starts with executing the save function of section key and user key which generates the anonymized values for sessionkeys and userkeys
    def save(self):
        self.sectionKey.save()
        self.userKey.save()

    #the anaonymized user ids in userkeys.txt are printed
    def print(self):
        print("*****")
        print("*** ANONYMIZATION KEY ***")
        self.userKey.print()
