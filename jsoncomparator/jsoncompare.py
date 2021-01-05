from typing import Tuple, Dict, List, Any
import json
from multimethod import multimethod

class Comparator():
    def __init__(self):
        pass
     
    @multimethod
    def compare(self, list_one: List, list_two: List) -> Tuple[bool, Dict]:
        return self._compare_lists(list_one, list_two)
    
    @multimethod
    def compare(self, dict_one: Dict, dict_two: Dict) -> Tuple[bool, Dict]:
        return self._compare_dicts(dict_one, dict_two)

    @multimethod
    def compare(self, one: Any, two: Any):
        raise TypeError

    def _compare_lists(self, list_one: List, list_two: List) -> Tuple[bool, Dict]:
        status = True
        details = {}

        for i in range(0, len(list_one)):
            diff = list_one.count(list_one[i]) - list_two.count(list_one[i])
            if diff > 0 and list_one[i] not in details.setdefault('removed',[]):
                status = False
                details['removed'].extend([list_one[i]] * diff)
            
        for i in range(0, len(list_two)):
            diff = list_two.count(list_two[i]) - list_one.count(list_two[i])
            if  diff > 0 and list_two[i] not in details.setdefault('added',[]):
                status = False
                details['added'].extend([list_two[i]] * diff)

        return status, details

    def _compare_dicts(self, dict_one: Dict, dict_two: Dict) -> Tuple[bool, Dict]:
        status = True
        details = {}

        keys = set().union(dict_one, dict_two)

        for name in keys:
            if name not in dict_one:
                details.setdefault('added', {})[name] = dict_two[name]
                status = False
            
            elif name not in dict_two:
                details.setdefault('removed', {})[name] = dict_one[name]
                status = False
            
            else:
                s, res = self._compare_element(dict_one[name], dict_two[name])
                if s is False:
                    details.setdefault('changed',{})[name] = res
                    status = False
        
        return status, details

    @multimethod
    def _compare_element(self, old: Dict, new: Dict) -> Tuple[bool, Dict]:
        return self._compare_dicts(new, old)

    @multimethod
    def _compare_element(self, old: List, new: List) -> Tuple[bool, Dict]:
        return self._compare_lists(old, new)

    @multimethod
    def _compare_element(self, old: Any, new: Any) -> Tuple[bool, Dict]:
        if type(old) == type(new) and old == new:
            return True, {}
        else:
            return False, {'old': old, 'new': new}
