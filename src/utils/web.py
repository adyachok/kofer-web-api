import re


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


def to_underscores(dict_obj):

    def convert(key):
        substr = re.findall('[A-Z][^A-Z]*', key)
        substr.insert(0, key[:len(key) - len(''.join(substr))])
        return '_'.join(substr).lower() if len(substr) else key

    request_dict = {}
    for key, val in dict_obj.items():
        key = convert(key)
        if isinstance(val, dict):
            request_dict[key] = to_underscores(val)
        elif isinstance(val, list):
            request_dict[key] = [to_underscores(item) for item in val]
        else:
            request_dict[key] = val
    return request_dict
