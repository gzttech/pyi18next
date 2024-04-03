import re
import json


class Translate:
    def __init__(self, i18next):
        self._i18next = i18next
        self._set_patterns()

    def _set_patterns(self):
        quote = r'(?:\'|\")'
        itpl_delim_beg = re.escape('{{')
        itpl_delim_end = re.escape('}}')
        nest_delim_beg = re.escape('$t(')
        nest_delim_end = re.escape(')')
        comma_delim = r'(?:\s*,\s*)'  # comma with optional spaces
        json_pattern = r'(?P<json>\{.*?\})?'
        param_name = r'(?:\s*;?\s*[\w]+)'
        param_format = r'(?: (?:[\d]+) | (?:\'.+\') | (?:[\d]+\.[\d]*))'
        param_default = fr'(?:\s*:\s*{param_format})?'
        func_pattern = fr'(?:(?:\w+)\((?P<params>(?:{param_name}{param_default})*)\))'
        param_pairs = fr'(?:{param_name}{param_default})'
        func_pattern_named = fr'(?:(?P<func_name>\w+)\((?P<params>(?:{param_name}{param_default})*)\))'
        func_list_pattern = fr'(?P<func_list>(?:{comma_delim}{func_pattern})*)'
        identifier = r'[\w\.]+'
        self.pattern_params = re.compile(param_pairs, re.VERBOSE)
        self.pattern_func = re.compile(func_pattern_named, re.VERBOSE)
        self.pattern = re.compile(fr"""
        (?:
          {itpl_delim_beg}(?P<itpl>{identifier}){func_list_pattern}{itpl_delim_end}
        ) |
        (?:
          {nest_delim_beg}(?P<nest>{identifier})(?:{comma_delim}{json_pattern})?{nest_delim_end}
        )
        """, re.VERBOSE)

    def parse_params(self, params):
        ret = {}
        for param_mo in self.pattern_params.finditer(params):
            ret[param_mo.group('param_name')] = param_mo.group('param_default')
        return ret
    
    def parse_func(self, func_list):
        ret = []
        for func_mo in self.pattern_func.finditer(func_list):
            ret.append(
                (func_mo.group('func_name'), self.parse_params(func_mo.group('params')))
            )
        return ret

    def handle_itpl(self, mo, **kwargs):
        identifier = mo.group('itpl')
        func_list = mo.group('func_list')
        if func_list:
            func_list = self.parse_func(func_list)
        print(identifier, func_list)
        value = kwargs.get(identifier)
        return value
    
    def handle_nest(self, mo, **kwargs):
        identifier = mo.group('nest')
        json_data = mo.group('json')
        if json_data:
             json_data = json.loads(json_data)
        else:
            json_data = {}
        print(identifier, json_data)
        return self._i18next.t(identifier, **json_data)

    def translate_str(self, value, **kwargs):
        def _sub_replace(mo):
            print(mo.groupdict())
            if mo.group('itpl'):
                return self.handle_itpl(mo, **kwargs)
            elif mo.group('nest'):
                return self.handle_nest(mo, **kwargs)
            raise ValueError(f"Invalid match object: {mo}")
        ret = self.pattern.sub(_sub_replace, value)
        return ret
    
    def translate_object(self, value, **kwargs):
        ret = {}
        for k, v in value.items():
            ret[k] = self.translate_value(v, **kwargs)
        if kwargs.get('return_objects') or self._i18next._options.get('return_objects'):
            return ret
        else:
            return None
    
    def translate_array(self, value, **kwargs):
        ret = []
        join_arrays = kwargs.pop('joinArrays', None) or self._i18next._options.get('join_arrays')
        for v in value:
            ret.append(self.translate_value(v, **kwargs))
        if join_arrays is not None:
            return join_arrays.join(ret)
        elif kwargs.get('return_objects') or self._i18next._options.get('return_objects'):
            return ret
        else:
            return None
    
    def translate_value(self, value, **kwargs):
        if isinstance(value, str):
            return self.translate_str(value, **kwargs)
        elif isinstance(value, dict):
            return self.translate_object(value, **kwargs)
        elif isinstance(value, list):
            return self.translate_array(value, **kwargs)
        else:
            return value

