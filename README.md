# jsoncomparator

## Run tests
python setup.py pytest  
or  
python -m pytest

## Build wheel package
python setup.py bdist_wheel

## Usage
```python
import json
from jsoncomparator.jsoncompare import Comparator

if __name__ == '__main__':
    with open('testB1.json') as f:
        json1 = json.load(f)
    
    with open('testB2.json') as f:
        json2 = json.load(f)   
    c = Comparator()
    status, details = c.compare(json1,json2)
```
## Samples

**List comparsion:**
```
json1 = {'a':[1,3,4,5,5]}
json2 =  {'a':[1,2,1,7,3,7]}
```

details:  
```
{'changed': {'a': {'added': [1, 2, 7, 7], 'removed': [4, 5, 5]}}}
```
**Dictionary comparsion:**
```  
json1 = {'person':{'name':'David', 'age': 23}}
json2 ={'person':{'name':'David', 'gender': 'male'}}
```
details:
```
{'changed': {'person': {'removed':{'age': 23}, 'added':{'gender': 'male'}}}}
```
