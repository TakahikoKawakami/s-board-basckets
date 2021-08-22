import re


def categorizeByKey(key, dictList):
    """"辞書型リストから、keyごとにリストを整理します
        [ { "a": 1, "b": 4 }, { "a": 2, "b": 5 }, { "a": 1, "b": 6 }, ]
        ↓
        {
            "1":[ { "a": 1, "b": 4 }, { "a": 1, "b": 6 }, ],
            "2":[ { "a": 2, "b": 5 }, ]
        }
    """

    result = {}
    for dictionary in dictList:
        if not (dictionary[key] in result.keys()):
            result[dictionary[key]] = []
        result[dictionary[key]].append(dictionary)

    return result


def getByKey(_key, _dict):
    return _dict.get(_key)


def convert_key_to_snake(d: dict) -> dict:
    result = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = convert_key_to_snake(v)
        if isinstance(v, list):
            v = [convert_key_to_snake(each_v) for each_v in v]
        result[_camel_to_snake(k)] = v

    return result


def convert_key_to_camel(d: dict) -> dict:
    result = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = convert_key_to_camel(v)
        result[_snake_to_camel(k)] = v

    return result


def _camel_to_snake(s: str) -> str:
    return re.sub("((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))", r"_\1", s).lower()


def _snake_to_camel(s: str) -> str:
    return re.sub("_(.)", lambda x: x.group(1).upper(), s)
