# Anonymizing the Sessions

Documentation Contributers:
- Anushree Manoharrao (documentation) Spring 2022

Documentation Editor and Reviewer:
- Mihai Boicu

## Understanding how to configure the class Session Key

The class SessionKey (stored in session_key.py) is managing a dictionary to anonymize a session in GMU format to a number that will hide when a course took place, but keeping the chronological order not changed. For instance, 202140 is the GMU format for a sesssion, which correspond to Summer 2021 and a possible generated anonymized code may be 237. For Fall 2021, 202170 a  generated anonymized code may be 314, but cannot be 129 (because will not maintain the chronological order).

There are several files asssociated with sessions:
- config/session-config.json: keeps the configuration data on how to generate the anonymized values for the sessions
- key/sessionKeys.txt: keeps the current generated anonymized values for the sessions (if the dictionary was generated in text format)
- key/sessionKeys.csv: keeps the current generated anonymized values for the sessions (if the dictionary was generated in CSV format)

Before you use session keys, you must define the configuration file. However, you must not define the key file, because this will be generated automatically by the code.

### Sample session-config.json
This file must contain values for all the following, as in the example below:
- The format is either TXT or CSV and indicates how the output is stored. 
- The start year and end year are inclusive and specify the range for which the anonymized session values are defined.
- List of semesters, contains the current GMU semesters, where 10,40,70 are Spring, Summer and Fall respectively.
- To randomize the session values, a start value along with a range for min and max step is used. The first key will start after the start key and for each next session (chronologically) a random value between min and max (inclusive) will be added. 

```
{ 
 "format": "TXT:,
 "start_year": 2004, 
 "end_year": 2030,
 "semesters_list": [10, 40, 70],
 "start_key": 100,
 "min_step": 10,
 "max_step": 100
}
```

### Sample of output in sessionKeys.txt
```
200040 198
200070 250
```
These numbers were generated as follows:
 - 200040 198   - Summer of 2000 is mapped to a number greater than 100 by adding a random value between 10 and 100 (e.g. 98), obtaining 198
 - 200070 250   - Fall of 2000 will be mapped to a number greater than 198 to which we added a random value between 10 and 100

The new anonymized values are added in the same chronological pattern as seen above.

### File location

- session-config.json has to be created under a new folder <strong>config</strong> under the root path of the project with a path like  "../config/session-config.json"
- sessionKeys.txt will be generated under the same root path with a new folder <strong>key</strong> with a path like  "../key/sessionKeys.txt"

## Understanding how to call the class Session Key

To use the anonymized sessions you must:
- import the class
```
import session_key;
```
- create only one instance of the class (do not duplicate the call)
```
sessionKey = session_key.SessionKey()
```

This will create an instance and load or initialize its anonymization dictioary. To obtain the anonymized value for a given session (e.g. 201040) you will call:
```
anonymizedSessionCode = self.sessionKey.dictionary[sessionCode]
```

## Understanding how the class SessionKey is coded

### Class initialization

If the sessionsKeys.txt file exists, 
- then the function <strong>load</strong> is executed. 
- else, <strong> generate </strong> and <strong> save </strong> functions are executed in that order. 

```
    def __init__(self):
        if os.path.isfile(self.KEY_FILE_NAME):
            self.load()
        else:
            self.generate()
            self.save()
```          

### Function: load


```
    def load(self):
        file = open(self.KEY_FILE_NAME)
        lines = file.readlines()
        for line in lines:
            parts = line.split(" ")
            self.dictionary[int(parts[0])] = int(parts[1])
        file.close()
```
The load function is performing the following operations:
- It opens the sessionKeys.txt that contains the anonymized values for the sessions and reads it line by line 
```
        file = open(self.KEY_FILE_NAME)
        lines = file.readlines()
        for line in lines:
```
- Each line looks like "200410 166", it has the actual session on its first and the second part has the anonymized value for that session.
- Each of these lines are split based on space and saved in dictionary as a key-value pair where actual session is key and its corresponding anonymized number is the value.
- For the above session the parts would look like ['200410', '166'], where parts[0] is the key with 200410 and parts[1] is it's value with 166.
```
            parts = line.split(" ")
```
- All of the session values are stored in the dictionary associating the anonymized code to the original session. 
```
            self.dictionary[int(parts[0])] = int(parts[1])
```

### The generate function is performing the following operations:
<ul>
  <li>  It uses the <strong>session-config.json</strong> file to generate the sessionkey.txt file </li>
  <li>  It opens and loads the session-config.json file </li>
  <li>  Generates the sessionkeys for the duration mentioned in the start_year and end_year of json file, e.g., from 2000 to 2030 </li>
  <li>  It generates two values and is stored as a dictionary using the below technique
    <ul>
      <li>  The first value which is the anonymizing the year is generated by performing (year*100) +sem </li>
      <li>  Second value which is a key to each year is generated by adding the previous key to a randomly generated integer between the defined range of minstep and         maxstep, incrementing it for every year in chronological order </li> 
    </ul>
  </li>
  <li>  The generated dictionary is saved by executing the “save” function </li>
</ul>

### The save functions is performing the following operations:
<ul>
 <li>  It creates a new file by writing to sessionkeys.txt file. </li>
 <li>  It does so by reading from the dictionary that was generated,  based on keys sorted in order</li>
 <li>  It then appends the session as key and the corresponding anonymized value as value to a single line, using space as delimiter.</li>
 <li>  This is exactly reverse of what happened in the load function. Load function first reads the line and splits it to key-value pair, and here it reads the key-value pair to make it a single value. </li>
</ul>