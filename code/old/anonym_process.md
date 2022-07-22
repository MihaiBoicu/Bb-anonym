# The Anonym Process

Contributers:
- Mouhamed Sylla (documentation) Spring 2022

Editor and reviewer:
- Mihai Boicu

## Understanding how to configure the class anonym_process
```
 inboxFolder = '../inbox/'
    outboxFolder = '../outbox/'
    archiveFolder = '../archive/'
```

## Functions in anonym_process
```
    def initInboxFiles(self):
    def initOutboxFolder
    def __init__(self):
    def __init__(self):
```

##Understanding how to call anonym_process
```
 key = AnonymKey()
 ```

##Understanding how to anonym_process class is coded
```
   with open(outboxFile, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in data:
                writer.writerow(row)
```
