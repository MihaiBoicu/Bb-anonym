
import os

from dictionary.session import session_key
from dictionary.section import section_key
from dictionary.user import user_key
from dictionary.assignment import assignment_key

class AllKeys:

    projectDirName: str = None
    projectName: str = None
    projectPath : str = None
    configPath : str = None
    keyPath : str = None
    inboxPath : str = None
    outboxPath : str = None
    
    sessionKey : session_key.SessionKey = None
    sectionKey : section_key.SectionKey = None
    userKey: user_key.UserKey = None
    assignmentKey: assignment_key.AssignmentKey = None

    def setName(self, name):
        self.projectName = name

    def initSessionKey(self):
        if self.sessionKey==None:
            self.sessionKey = session_key.SessionKey(self.projectPath)

    def initSectionKey(self):
        if self.sectionKey==None:
            self.initSessionKey()
            self.sectionKey = section_key.SectionKey(self.projectPath, self.sessionKey)

    def initUserKey(self):
        if self.userKey==None:
            self.userKey = user_key.UserKey(self.projectPath)

    def initAssignmentKey(self):
        if self.assignmentKey==None:
            self.assignmentKey = assignment_key.AssignmentKey(self.projectPath)

    def _initFolder(self,folderPath):
        if not os.path.exists(folderPath):
            os.mkdir(folderPath)

    def _initFolders(self):
        self._initFolder(self.inboxPath)
        self._initFolder(self.keyPath)
        self._initFolder(self.outboxPath)

    def save(self):
        if self.sectionKey!=None:
            self.sectionKey.save()
        if self.userKey!=None:
            self.userKey.save()

    def __init__(self, projectDirName, projectPath):
        self.projectDirName=projectDirName
        self.projectPath=projectPath
        self.configPath = self.projectPath + "/config"
        self.keyPath = self.projectPath + "/key"
        self.inboxPath = self.projectPath + "/inbox"
        self.outboxPath = self.projectPath + "/outbox"
        self._initFolders()
        

