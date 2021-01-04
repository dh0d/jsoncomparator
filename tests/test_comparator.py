import pytest
from jsoncomparator import jsoncompare

@pytest.fixture
def comparator():
    inst = jsoncompare.Comparator() 
    yield inst

def test_with_empty(comparator):
    status, details = comparator.compare({},{})
    assert status == True
    assert details == {}
    
    status, details = comparator.compare({},{1:1})
    assert status == False
    assert details == {'added':{1:1}}

    status, details = comparator.compare({1:1},{})
    assert status == False
    assert details == {'removed':{1:1}}

    status, details = comparator.compare([],[])
    assert status == True
    assert details == {}

    status, details = comparator.compare([{}],[{}])
    assert status == True
    assert details == {}

    status, details = comparator.compare([{}],[{},{}])
    assert status == False
    assert details == {'new': [{},{}], 'old': [{}]}

    with pytest.raises(TypeError):
        status, details = comparator.compare([],{})

def test_nested(comparator):
    status, details = comparator.compare({'a':'b'}, {'a':'b', 'c':'d'})
    assert status == False
    assert details == {'added':{'c':'d'}}
    
    status, details = comparator.compare({'a':'b', 'c':'d'}, {'a':'b'})
    assert status == False
    assert details == {'removed':{'c':'d'}}

def test_diff_value(comparator):
    status, details = comparator.compare({'a':'b'}, {'a':'c'})
    assert status == False
    assert details == {'changed': {'a': {'new': 'c', 'old': 'b'}}}
    
    status, details = comparator.compare({'a':'b'}, {'a': 1})
    assert status == False
    assert details == {'changed': {'a': {'new': 1, 'old': 'b'}}}
    
    status, details = comparator.compare({'a':'b'}, {'a': []})
    assert status == False
    assert details == {'changed': {'a': {'new': [], 'old': 'b'}}}
    
    status, details = comparator.compare({'a':['b']}, {'a': ['c']})
    assert status == False
    assert details == {'changed': {'a': {'new': ['c'], 'old': ['b']}}}

    status, details = comparator.compare({'a':['b']}, {'a': {'b'}})
    assert status == False
    assert details == {'changed': {'a': {'new': {'b'}, 'old': ['b']}}}
    
def test_with_null(comparator):
    status, details = comparator.compare({'a':None},{'a': None})
    assert status == True
    assert details == {}
    
    status, details = comparator.compare({'a':None},{'a': ''})
    assert status == False
    assert details == {'changed': {'a': {'new': '', 'old': None}}}

def test_diff_list(comparator):
    status, details = comparator.compare({'a':['b']}, {'a':['c']})
    assert status == False
    assert details == {'changed': {'a': {'new': ['c'], 'old': ['b']}}}

    status, details = comparator.compare({'a':[1]}, {'a':[2]})
    assert status == False
    assert details == {'changed': {'a': {'new': [2], 'old': [1]}}}

    status, details = comparator.compare({'a':[1]}, {'a':[1, 2]})
    assert status == False
    assert details == {'changed': {'a': {'new': [1, 2], 'old': [1]}}}

    status, details = comparator.compare({'a':[1, 2]}, {'a':[2, 1]})
    assert status == False
    assert details == {'changed': {'a': {'new': [2, 1], 'old': [1, 2]}}}

def test_deep_diff(comparator):
    status, details = comparator.compare({'a1':{'a2':{'a3':'b'}}}, {'a1':{'a2':{'a3':'c'}}})
    assert status == False
    assert details == {'changed': {'a1': {'changed':{'a2':{'changed':{'a3':{'new':'c', 'old': 'b'}}}}}}}
