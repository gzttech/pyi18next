'''
Format functions for i18next.
'''
import babel.numbers
import babel.dates
import babel.lists


FUNCTIONS = {
    'number': babel.numbers.format_decimal,
    'currency': babel.numbers.format_currency,
    'format_compact_currency': babel.numbers.format_compact_currency,
    'format_compact_decimal': babel.numbers.format_compact_decimal,
    'format_currency': babel.numbers.format_currency,
    'format_decimal': babel.numbers.format_decimal,
    'format_number': babel.numbers.format_number,
    'format_percent': babel.numbers.format_percent,
    'format_scientific': babel.numbers.format_scientific,
    'datetime': babel.dates.format_datetime,
    'relativetime': babel.dates.format_timedelta,
    'format_date': babel.dates.format_date, 
    'format_datetime': babel.dates.format_datetime,
    'format_interval': babel.dates.format_interval,
    'format_skeleton': babel.dates.format_skeleton,
    'format_time': babel.dates.format_time,
    'format_timedelta': babel.dates.format_timedelta,
    'list': babel.lists.format_list,
    'format_list': babel.lists.format_list,
}


def parse_param_default_value(param_default_value):
    '''
    Parse a parameter default value in a format function.
    '''
    if param_default_value is None:
        return None
    if param_default_value.startswith("'") and param_default_value.endswith("'"):
        return param_default_value[1:-1]
    if param_default_value == 'true':
        return True
    if param_default_value == 'false':
        return False
    if '.' in param_default_value:
        return float(param_default_value)
    return int(param_default_value)


def apply_function(value, function_desc, **params):
    '''
    Apply a format function to a value.
    '''
    function_name, function_params = function_desc
    if function_name not in FUNCTIONS:
        raise ValueError(f'Unknown function: {function_name}')
    func = FUNCTIONS[function_name]
    func_annotations = getattr(func, '__annotations__', {})
    default_params = {}
    for param_name, param_default_value in function_params.items():
        if param_default_value is None:
            continue
        param_default_value = parse_param_default_value(param_default_value)
        if param_name in func_annotations:
            param_type = func_annotations[param_name]
            default_params[param_name] = param_type(param_default_value) if callable(param_type) else param_default_value
        else:
            default_params[param_name] = param_default_value
    call_params = {**default_params, **params}
    return func(value, **call_params)


