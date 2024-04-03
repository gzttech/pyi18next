import re
import typing
import babel.plural

def merge_list(*args):
    '''
    Merge the lists into one list.
    '''
    ret = []
    for arg in args:
        if not arg:
            continue
        elif isinstance(arg, (list, tuple)):
            ret.extend(arg)
        else:
            ret.append(arg)
    return ret


def match_lng(lng1: str, lng2: str, ignore_case: bool=True, implicit: bool=False):
    '''
    Check if the two language codes match.
    '''
    if ignore_case:
        lng1, lng2 = [i.lower() for i in [lng1, lng2]]
    if not implicit:
        return lng1 == lng2
    else:
        short_lng, long_lng = sorted([lng1, lng2], key=len)
        return long_lng.startswith(short_lng)


def get_deep_value(obj, keys, default=None):
    '''
    Get a value from obj based on a chain of keys.
    '''
    value = default
    curr = obj
    for key in keys:
        if isinstance(curr, dict) and key in curr:
            value = curr[key]
            curr = value
        elif isinstance(curr, (list, tuple)) and (isinstance(key, int) or key.isdigit()):
            value = curr[int(key)]
            curr = value
        else:
            return default
    return value

def get_plural_func(rules: typing.Union[str, dict]):
    '''
    Get the plural rules object from the rules string.
    '''
    rule_func = None
    rule_dict = {}
    if isinstance(rules, str):
        for rule in rules.split(';'):
            if not rule.strip():
                continue
            key, value = rule.split(':')
            key = key.strip()
            value = value.strip()
            rule_dict[key] = value
    elif isinstance(rules, dict):
        rule_dict = rules
    if rule_dict:
        rule_func = babel.plural.PluralRule(rule_dict)
    return rule_func
