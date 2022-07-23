# Author: Mihai Boicu

# from dictionary.session import session_key_test
# from dictionary.section import section_key_test
# from dictionary.user import user_key_test
import json
from dictionary.project import project

class ProjectDir:
    name:None
    path:None

    def __init__(self, name, path):
        self.name = name
        self.path = path

# Manage the list of available projects 
class ProjectsList:

    _DEBUG = False

    _projectsFilename = None

    _repository = None
    _projectsList = []

    def _load(self):
        configFile = open(self._projectsFilename, mode='r')
        configData = json.load(configFile)
        configFile.close()

        self._repository = configData['repository']
        projects = configData['projects']
        for projectJson in projects:
            projectDir = ProjectDir(projectJson['name'],  projectJson['path'])
            self._projectsList.append(projectDir)


    def interactive(self):
        print("Repository: "+str(self._repository))
        while True:
            print('\nSelect a project:')
            noProjects = 0
            for pd in self._projectsList:
                noProjects += 1
                print(" "+str(noProjects)+". "+str(pd.name))     
            print(" 0. exit")
            selection = int(input('>>> '))
            if selection==0:
                break
            if selection<0 or selection>noProjects:
                print('Invalid selection')
                continue
            p = project.Project(self._projectsList[selection-1].name, self._projectsList[selection-1].path)
            p.execute()
            # print("Selection "+str(selection)+" "+str(self._projectsList[selection-1].name)+" "+str(self._projectsList[selection-1].path))

    def __init__(self, projectListFilename):
        self._projectsFilename = projectListFilename
        self._load()
        