import pyi18next.i18next

RESOURCES = {
    'en': {
        'translation': {
            'key': 'value',
            'object': {"key": "value"},
            'array': ['value1', 'value2'],
            'interpolation': 'Hello, {{name}}!',
            'object_interpolation': {'greet': 'Hello, {{name}}!'},
            'array_interpolation': ['Hello', '{{name}}', '!'],
            'nested': '$t(key)',
            'nested_interpolation': '$t(interpolation, {"name": "Friend"})',
            'key_male': 'mail value',
            'key_female': 'female value',
            'keyPlural_one': 'one',
            'keyPlural_two': 'two',
            'keyPlural_other': 'other',
            'numberFormat': "Number: {{val, number(format: '0.00')}}",
            'datesFormat': "Datetime: {{val, datetime(format: 'yyyy-MM-dd')}}",
            'listFormat': "List: {{val, list(style: 'or')}}",
        },
        'special': { 
            'key': 'special value',
        }
    }
}

i18n = pyi18next.i18next.I18next(
            resources=RESOURCES,
            default_lng='en',
            default_ns='translation',
            plural_rules='one: n is 1; two: n is 2')

class TestTranslate:
    def test_base(self):
        assert i18n.t('key') == 'value'

    def test_deep(self):
        assert i18n.t('object.key') == 'value'

    def test_default(self):
        assert i18n.t('keyinexisted', 'default value') == 'default value'

    def test_cimode(self):
        assert i18n.t('key', lng='cimode') == 'key'
        assert i18n.t('key', lng='cimode', append_namespace_to_cimode=True) == 'translation:key'

    def test_special(self):
        assert i18n.t('key', ns='special') == 'special value'
        assert i18n.t('special:key') == 'special value'
    
    def test_object(self):
        assert i18n.t('object', return_objects=True) == {"key": "value"}
    
    def test_array(self):
        assert i18n.t('array', return_objects=True) == ['value1', 'value2']
        assert i18n.t('array', joinArrays=' ') == 'value1 value2'
    
    def test_interpolation(self):
        assert i18n.t('interpolation', name='world') == 'Hello, world!'
        assert i18n.t('object_interpolation', name='world', return_objects=True) == {'greet': 'Hello, world!'}
        assert i18n.t('array_interpolation', name='world', return_objects=True) == ['Hello', 'world', '!']
        assert i18n.t('array_interpolation', name='world', joinArrays=' ') == 'Hello world !'

    def test_nest(self):
        assert i18n.t('nested') == 'value'
        assert i18n.t('nested_interpolation') == 'Hello, Friend!'

    def test_context(self):
        assert i18n.t('key_male') == 'mail value'
        assert i18n.t('key_female') == 'female value'

    def test_plural(self):
        assert i18n.t('keyPlural', count=1) == 'one'
        assert i18n.t('keyPlural', count=2) == 'two'
        assert i18n.t('keyPlural', count=3) == 'other'

    def test_format(self):
        assert i18n.t('numberFormat', val=1024) == 'Number: 1024.00'
        import datetime
        assert i18n.t('datesFormat', val=datetime.datetime(2000,1,1)) == 'Datetime: 2000-01-01'
        assert i18n.t('listFormat', val=[1, 2, 3, 4]) == 'List: 1, 2, 3, or 4'