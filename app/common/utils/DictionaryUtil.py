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
    if _key in _dict:
        return _dict[_key]
    return None