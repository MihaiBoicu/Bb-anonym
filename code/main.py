# Author: Mihai Boicu

# python main.py


from dictionary.project import projects_list


def main():
    list = projects_list.ProjectsList("../project/projects.json")
    list.interactive()

if __name__ == '__main__':
    main()