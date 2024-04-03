import os.path
import typing
from .. import loaders


class  Backend:
    def __init__(self, name_mapping=None):
        '''
        Initialize the backend with the name mapping function.
        name_mapping: a function that maps the namespace to the file name.
        '''
        self.set_name_mapping(name_mapping)

    def set_name_mapping(self, name_mapping):
        if isinstance(name_mapping, dict):
            self.name_mapping = lambda lng, ns: name_mapping.get(ns, ns)
        elif callable(name_mapping):
            self.name_mapping = name_mapping
        else:
            self.name_mapping = lambda lng, ns: ''        

    def read_one(self, lng: str, ns: str):
        '''
        Read the translation data from the file.
        '''
        filename = self.name_mapping(lng, ns)
        file_name, file_ext = os.path.splitext(filename)
        file_type = file_ext[1:].lower()
        with open(filename, 'r') as f:
            data = loaders.load_data(f, file_type)
        return data
    
    def read_all(self, lng_list: typing.List, ns_list: typing.List):
        '''
        Read all the translation data from the files.
        '''
        ret = {}
        for lng in lng_list:
            for ns in ns_list:
                ret[(lng, ns)] = self.read_one(lng, ns)
        return ret