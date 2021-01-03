import ast
import ujson
import pyfpgrowth as fp

class Pyfpgrowth():
    """pyfpgrowth entity
        インスタンス化せず、createXXX系を用いて作成すること
    """
    def __init__(self, val):
        self._patterns = val # pyfpgrowthの生データ


    @staticmethod
    def createAndfindFrequentPatterns(_list, _count):
        _patterns = fp.find_frequent_patterns(_list, _count)
        result = Pyfpgrowth(_patterns)
        return result


    @staticmethod
    def createByJson(_json):
        _loadedList = ujson.loads(_json)
        _result = {}
        for _eachDict, val in _loadedList.items():
            _result[ast.literal_eval(_eachDict)] = val

        return Pyfpgrowth(_result)


    @property
    def patterns(self):
        return self._patterns


    @property
    def stringPatterns(self):
        return ujson.dumps(self._patterns)


    def merge(self, _pyfpgrowthEntity):
        """当entityに、PyfpgrowthEntityをマージします
        同じキーの場合はvalueを加算します

        Arguments:
            _pyfpgrowthEntity {Pyfpgrowth} -- [description]

        Returns:
            [type] -- [description]
        """
        for key, value in _pyfpgrowthEntity.patterns.items():
            if not key in self._patterns.keys():
                self._patterns[key] = 0
            self._patterns[key] += value

        return self


    def convertToVisJs(self):
        edges = []
        nodes = []
        for k,v in self._patterns.items():
            if (len(k) == 1):
                if (k[0].startswith('product__')): # product__{"id": xxx, "name": xxx, "categoryId": xxx}
                    productJson = k[0].split('product__')[1]
                    productDict = ujson.loads(productJson)
                    nodes.append({
                        "id"   : productDict['id'],
                        "label": productDict['id'],
                        "value": v
                    })
            elif (len(k) == 2):
                if (k[0].startswith('product__') and k[1].startswith('product__')):
                    productJsonList = []
                    productDictList = []
                    productJsonList.append(k[0].split('product__')[1])
                    productDictList.append(ujson.loads(productJsonList[-1]))
                    productJsonList.append(k[1].split('product__')[1])
                    productDictList.append(ujson.loads(productJsonList[-1]))
                    edges.append({
                        "from": productDictList[0]['id'],
                        "to"  : productDictList[1]['id'],
                        "value": v
                    })
    
        return {"nodes": nodes, "edges": edges}
