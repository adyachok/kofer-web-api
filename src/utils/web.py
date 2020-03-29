def to_camel_case(dict_obj):
    json_dict = {}
    for key, val in dict_obj.items():
        if '_' in key and not key.startswith('_'):
            for i, c in enumerate(key):
                if c == '_':
                    key = key[:i] + key[i+1:].capitalize()
            key = key.replace('_', '')
        if isinstance(val, dict):
            json_dict[key] = to_camel_case(val)
        else:
            json_dict[key] = val
    return json_dict
