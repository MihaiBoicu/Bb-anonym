	# Anonymizing Assignments

Contributers:
- Mouhamed Sylla (Documentation) Spring 2022

Editor and reviewer:
- Mihai Boicu

## Understanding how to configure the Assignment key


The class AssignmentKey is used to randomize the assignments of a GMU course. This code will be randomized using the anonymized key from the json. Purpose of this randomizing process is to change the name of assignments to not make it easy for others to understand what grade came from what assignment, to do this one must define the configuration file.
After randomization one must check if there are predefined names, if the name is the same grade is a 0 on the anonym assignment.
-Specific files asssociated with assignmentkey: 
- config/session-config.json: keeps the configuration data on how to generate the anonymized values for the assignments

## Understanding how the class Assignmentkey is coded

The class is meant to randomized assignments from each other so after the randomization process of the names become a list. There is also the term points which represent the grade given on an assignment.  The code used is…
```
def getGC(self,gcName):
	        pointsSplit = gcName.split("[")
	        pointsPart = pointsSplit[1].split(' ')[2]
	        points = 0.0
	        if pointsPart == 'up':
	            points = float(pointsSplit[1].split(' ')[4])
	        else:
	            points = float(pointsPart)      
	

	        nameSplit = pointsSplit[0].split('-')[0].split('(')[0]
	        name = str(nameSplit).strip()  # + ' [' + points + ']'
	        if points == 0:
	            points == self.defaultTotalZeroPoints
	        if name in self.dictionary:
	            return self.dictionary[name], points
```
pointsSplit is used and it turns gcName into a list with its new values. If pointsParts == ‘up’ then the points given will be split, if not there will just be a float for the value.
Finally with this portion of code if points equal 0 it will be seen as the default value 0.

```
  Name=  qrName.strip()
	        if name in self.dictionary:
	            return self.dictionary[name]
	        else:
	            return "IGNORE"

```
The strip function is used here to delete any extra spaces on the name after randomization.

### Function: Load
```
  def load(self):
	        configFile = open(self.configurationFileName,)
	        configData = json.load(configFile)
```
## Sample of output in Assignment
Name: “D5 Cumlative test”
Code: “A061”

The randomization will change the name of something like “D5 Cumlative test” into
 “A061”
With subsequent assignments being anonymized the first letter will be randomized then the numbers will be going in sequential order.
