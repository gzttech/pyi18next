# pyi18next

[![Documentation Status](https://readthedocs.org/projects/pyi18next/badge/?version=latest)](https://pyi18next.readthedocs.io/en/latest/?badge=latest)

A Python implementation of [i18next](https://github.com/i18next/i18next). Documentation is available at [pyi18next.readthedocs.io](https://pyi18next.readthedocs.io).

## Quick Start

### Install

```
python -m pip install -U pyi18next
```

### Init

We can define a `I18next` object with translations loaded as follow:

```python
import pyi18next.i18next

i18n = pyi18next.i18next.I18next(
     resources={
        'en': {
            'translation': {
                'key': 'value',
                'interpolation': 'Hello, {{name}}!',
                'nested': '$t(key)',
            }
        }
    },
    default_lng='en',
    default_ns='translation'
)
```

### Translate

We can use the `i18n` object we defined to translate:

```python
print(f'{i18n.t("key")=}')
print(f'{i18n.t("interpolation", name="world")=}')
print(f'{i18n.t("nested")=}')
``` 

The results are:

```
i18n.t("key")='value'
i18n.t("interpolation", name="world")='Hello, world!'
i18n.t("nested")='value'
``` 
