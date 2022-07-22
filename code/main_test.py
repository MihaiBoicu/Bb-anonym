# python main_test.py

from dictionary.session import session_key_test
from dictionary.section import section_key_test
from dictionary.user import user_key_test

def main():
    print('Select a test:')
    print('  1. session')
    print('  2. section')
    print('  3. user')
    selection = int(input('>>> '))
    if selection==1:
        session_key_test.main()
    elif selection==2:
        section_key_test.main()
    elif selection==3:
        user_key_test.main()
    else:
        print('Invalid selection')


if __name__ == '__main__':
    main()