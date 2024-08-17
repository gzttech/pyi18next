# Get Started

Before we translate any text, we can define a `I18next` object as follow:

```python
import pyi18next.i18next

i18n = pyi18next.i18next.I18next(
    default_lng='en',
    default_ns='translation',
    resources= {
        'en': {
            'translation': {
                'key': 'value',
                'object': {"inner_key": "value deep"},
                'interpolation': 'Hello, {{name}}!',
           }
        }
    }
)
```

The translations are defined as key-value pairs in the `resources.en.tranlation` dictionary, where the language is `en` and the namespace is `translation`.

Then we can use `i18n.t` function to get translate:

```python
print(f'{i18n.t("key")=}')
print(f'{i18n.t("object.inner_key")=}')
print(f'{i18n.t("interpolation", name="world")=}')
```

The results are:

```
i18n.t("key")='value'
i18n.t("object.inner_key")='value deep'
i18n.t("interpolation", name="world")='Hello, world!'
```

Or we can use a global function `t_`

```python
t_ = i18n.get_translate_func()
print(f'{t_("key")=}')
print(f'{t_("object.inner_key")=}')
print(f'{t_("interpolation", name="world")=}')
```

The results are just the same:

```
t_("key")='value'
t_("object.inner_key")='value deep'
t_("interpolation", name="world")='Hello, world!'
```