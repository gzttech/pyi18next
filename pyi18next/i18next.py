import functools
import typing
import locale
from . import utility
from . import translate


class I18next:
    def __init__(self, **options):
        self.translation_map = {}
        self._options = {}
        self._plural_func = None
        self.update_options(**options)
        if self._options.get('init_immediate', True) and self._options.get('backend'):
            self.load()

    def update_options(self,
                       resources=None,
                       backend=None, 
                       init_immediate: bool = True,
                       lng: typing.Union[str, list, tuple]=None,
                       ns: typing.Union[str, list, tuple]=None,
                       default_lng=None,
                       default_ns=None,
                       fallback_lng: typing.Union[str, list, tuple]=None,
                       fallback_ns: typing.Union[str, list, tuple]=None,
                       plural_rules=None,
                       return_objects=False,
                       join_arrays=None,
                       **options):
        self._options.update({
            'resources': resources,
            'backend': backend,
            'init_immmediate': init_immediate,
            'lng': lng,
            'ns': ns,
            'default_lng': default_lng,
            'default_ns': default_ns,
            'fallback_lng': fallback_lng,
            'fallback_ns': fallback_ns,
            'plural_rules': plural_rules,
            'return_objects': return_objects,
            'join_arrays': join_arrays,
            **options})
        if self._options.get('plural_rules'):
            self._plural_func = utility.get_plural_func(self._options['plural_rules'])
        if self._options.get('resources'):
            self.translation_map = self._options.get('resources')
        self.translate = translate.Translate(self)

    def load(self):
        all_lngs = utility.merge_list(self._options.get('lng'),
                                      self._options.get('default_lng'), 
                                      self._options.get('fallback_lng'))
        all_ns = utility.merge_list(self._options.get('ns'),
                                    self._options.get('default_ns'),
                                    self._options.get('fallback_ns'))
        if backend := self._options.get('backend'):
            self.translation_map = backend.read_all(all_lngs, all_ns)

    def resolve_lng_ns(self, key_info, **kwargs):
        lng = kwargs.get('lng') or self._options.get('default_lng') or locale.getlocale()[0]
        ns = kwargs.get('ns') or key_info.get('ns') or self._options.get('default_ns')
        return (lng, ns)
    
    def resolve_translation(self, lng, ns, **kwargs):
        fallback_lng = self._options.get('fallback_lng') or []
        fallback_ns = self._options.get('fallback_ns') or []
        translation = None
        for curr_lng in utility.merge_list(lng, fallback_lng):
            for curr_ns in utility.merge_list(ns, fallback_ns):
                translation = utility.get_deep_value(self.translation_map, [curr_lng, curr_ns])
                if translation is not None:
                    break
        return translation
    
    def get_key_info(self, original_key, **kwargs):
        ret = {}
        key = original_key
        ns_splitted = key.split(':', maxsplit=1)
        # handle namespace
        if len(ns_splitted) == 2:
            ret['ns'] = ns_splitted[0]
            key = ns_splitted[1]
        if kwargs.get('context'):
            key = f'{key}_{kwargs["context"]}'
        if kwargs.get('count') and self._plural_func:
            key = f'{key}_{self._plural_func(kwargs["count"])}'
            print(key)
        # handle deep key
        ret['deep'] = key.split('.')
        ret['key'] = key
        return ret

    def t(self, key, *subs, **kwargs):
        ret = None
        key_info = self.get_key_info(key, **kwargs)
        (lng, ns) = self.resolve_lng_ns(key_info, **kwargs)
        translation = self.resolve_translation(lng, ns)
        print(f'{key_info=}, {kwargs=}')
        if translation:
            ret = self.translate.translate_value(translation.get(key_info['key']), **kwargs)
        if ret is None and subs:
            ret = subs[0]
        return ret

    def get_translate_func(self, **kwargs):
        return functools.partial(self.t, **kwargs)