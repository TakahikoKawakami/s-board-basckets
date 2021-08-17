def categorize_by_key(key, entity_list):
    """"entityリストから、entityのもつkeyで指定したメンバごとにリストを整理します
        [ { "a": 1, "b": 4 }, { "a": 2, "b": 5 }, { "a": 1, "b": 6 }, ]
        ↓
        {
            "1":[ { "a": 1, "b": 4 }, { "a": 1, "b": 6 }, ],
            "2":[ { "a": 2, "b": 5 }, ]
        }
    """

    result = {}
    for entity in entity_list:
        if not (getattr(entity, key) in result.keys()):
            result[getattr(entity, key)] = []
        result[getattr(entity, key)].append(entity)

    return result
