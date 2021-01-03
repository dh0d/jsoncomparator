import json
from multimethod import multimethod

class Comparator():
    def __init__(self):
        pass
     
    @multimethod
    def compare(self, list_one: list, list_two: list):
        return self._compare_lists(list_one, list_two)
    
    @multimethod
    def compare(self, dict_one: dict, dict_two: dict):
        return self._compare_dicts(dict_one, dict_two)

    @multimethod
    def compare(self, one, two):
        raise TypeError

    def _compare_lists(self, list_one: list, list_two: list):
        if list_one == list_two:
            return True, {}
        else:
            return False, {'old': list_one, 'new': list_two}

    def _compare_dicts(self, dict_one, dict_two):
        status = True
        details = {}

        keys = set(dict_one.keys()) | set(dict_two.keys())

        for name in keys:
            if name not in dict_one:
                if 'added' not in details: details['added'] = {}
                details['added'][name] = dict_two[name]
                status = False
            
            elif name not in dict_two:
                if 'removed' not in details: details['removed'] = {}
                details['removed'][name] = dict_one[name]
                status = False
            
            else:
                s, res = self._compare_element(dict_one[name], dict_two[name])
                if s is False:
                    details.setdefault('changed',{})[name] = res
                    status = False
        
        return status, details

    @multimethod
    def _compare_element(self, old: dict, new: dict):
        return self._compare_dicts(new, old)

    @multimethod
    def _compare_element(self, old: list, new: list):
        return self._compare_lists(old, new)

    @multimethod
    def _compare_element(self, old, new):
        if type(old) == type(new) and old == new:
            return True, {}
        else:
            return False, {'old': old, 'new': new}
