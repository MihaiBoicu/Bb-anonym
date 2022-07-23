# python main_test.py


from dictionary.projectsList import projects_list


def main():
    list = projects_list.ProjectsList("../test/projects.json")
    list.interactive()

if __name__ == '__main__':
    main()