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
