'''
This module contains the file format loaders for the pyi18next package.
'''


def load_data(file, file_type: str) -> dict:
    '''
    Load the data from the file.
    '''
    content = file.read() if hasattr(file, 'read') else file
    if file_type == 'json':
        import json
        return json.loads(content)
    elif file_type == 'yaml' or file_type == 'yml':
        import yaml
        return yaml.safe_load(content)
    else:
        raise ValueError(f'Unsupported file type: {file_type}')