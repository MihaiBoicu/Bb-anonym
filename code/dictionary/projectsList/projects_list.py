# Author: Mihai Boicu

# from dictionary.session import session_key_test
# from dictionary.section import section_key_test
# from dictionary.user import user_key_test
import json

class ProjectDir:
    name:None
    path:None

    def __init__(self, name, path):
        self.name = name
        self.path = path

# Manage the list of available projects 
class ProjectsList:

    _DEBUG = False

    _PROJECTS_FILENAME = None

    _REPOSITORY = None
    _PROJECTS_LIST = []

    def _loadProjectsList(self):
        configFile = open(self._PROJECTS_FILENAME, )
        configData = json.load(configFile)

        self._REPOSITORY = configData['repository']
        projects = configData['projects']
        for projectJson in projects:
            projectDir = ProjectDir(projectJson['name'],  projectJson['path'])
            self._PROJECTS_LIST.append(projectDir)


    def interactive(self):
        print("Repository: "+str(self._REPOSITORY))
        while True:
            print('\nSelect a project:')
            noProjects = 0
            for project in self._PROJECTS_LIST:
                noProjects += 1
                print(" "+str(noProjects)+". "+str(project.name))     
            print(" 0. exit")
            selection = int(input('>>> '))
            if selection==0:
                break
            if selection<0 or selection>noProjects:
                print('Invalid selection')
                continue
            print("Selection "+str(selection)+" "+str(self._PROJECTS_LIST[selection-1].name)+" "+str(self._PROJECTS_LIST[selection-1].path))

    def __init__(self, projectListFilename):
        self._PROJECTS_FILENAME = projectListFilename
        self._loadProjectsList()