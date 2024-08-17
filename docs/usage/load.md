# Loading Translation Files

You may use pyi8next to load i18next tranlation files in [JSON format](https://www.i18next.com/misc/json-format) or in YAML format of the same schema. For example,

```python
import pyi18next.i18next
import pyi18next.backends.fs as fs

i18n = pyi18next.i18next.I18next(
    lng=['en', 'fr'],
    ns=['translation', 'enum'],
    backend=fs.Backend(name_mapping=lambda lng, ns: f'example/{ns}/{lng}.json'))
i18n.load()
```

The example code will load translation files under `example` directory. The directory structure is like

```plaintext
example/
├── enum
│   ├── en.json
│   └── fr.json
└── translation
    ├── en.json
    └── fr.json
```

Here, `ns` means [namespaces](https://www.i18next.com/principles/namespaces), which is a way to group translations; `lng` means languages. The `name_mapping` function is used to map the language and namespace to the file path.
