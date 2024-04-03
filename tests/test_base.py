import pyi18next.i18next
import pyi18next.backends.fs as fs

def test_class():
    i18n = pyi18next.i18next.I18next()
    assert i18n

def test_load():
    import json
    backend = fs.Backend(name_mapping=lambda lng, ns: f'tests/sample/{ns}/{lng}.json')
    i18n = pyi18next.i18next.I18next(lng='en', ns='translation', backend=backend)
    i18n.load()
    i18n.t('key', lng='en', ns='translation') == 'value'