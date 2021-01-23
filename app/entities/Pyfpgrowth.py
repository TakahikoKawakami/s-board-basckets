from flask import session
import numpy as np
import itertools
from scipy.sparse import lil_matrix  # other types would convert to LIL anyway
import ast
import ujson
from orangecontrib.associate import fpgrowth as fp
import logging

from app.domains.ProductsRepository import ProductsRepository
from app.entities.VisJs import Node, Edge


class Pyfpgrowth():
    MAX_EDGE_COUNT = 300
    ASSOCIATION_RATE = 0.01
    """pyfpgrowth entity
        インスタンス化せず、createXXX系を用いて作成すること
    """
    def __init__(self):
        self._basketList = []
        self._patterns = [] # pyfpgrowthの生データ
        self._rules = [] # 出力の際に算出
        self._stats = []
        self._result = []
        
        self._logger = logging.getLogger("flask.app")


    @staticmethod
    def createByDataList(_list, _count):
        # 店舗情報をlistから取り除く
        # TODO 今後、店舗情報も分析対象に加えたい
        _list = Pyfpgrowth._removeStoreData(_list)
        _list = Pyfpgrowth._removeMemberData(_list)
        _list = Pyfpgrowth._removeSexData(_list)
        _list = Pyfpgrowth._removeStoreData(_list)

        pyfpgrowth = Pyfpgrowth()
        _numberKeyDict, _columnKeyDict = pyfpgrowth._getKeyDictionaries(_list)

        _encodedList = pyfpgrowth._encode(_list, _columnKeyDict)

        # X, mapping = fp.OneHot.encode(_list)
        itemsets = dict(fp.frequent_itemsets(_encodedList, 0.01))
        pyfpgrowth._patterns = itemsets
        # アソシエーションルールの抽出
        rules = fp.association_rules(itemsets, 0.6)
        pyfpgrowth._rules = rules
        # リフト値を含んだ結果を取得
        stats = fp.rules_stats(rules, itemsets, len(_encodedList))
        pyfpgrowth._stats = stats
        # リフト値（7番目の要素）でソート

        result = []
        if len(itemsets) > 0:
            for s in sorted(stats, key = lambda x: x[6], reverse = True):

                lhs = pyfpgrowth._decode(s[0], _numberKeyDict)
                rhs = pyfpgrowth._decode(s[1], _numberKeyDict)

                support = s[2]
                confidence = s[3]
                lift = s[6]

                # print(f"lhs = {lhs}, rhs = {rhs}, support = {support}, confidence = {confidence}, lift = {lift}")

                if lift < 1:
                    break

                result.append(
                    {
                        "from": lhs,
                        "to": rhs,
                        "support": support,
                        "confidence": confidence,
                        "lift": lift
                    }
                )
        pyfpgrowth._result = result
        return pyfpgrowth


    @staticmethod
    def _getKeyDictionaries(_list):
        # バスケット内に登場する全データを重複を除いて1行リストにまとめる
        _flatDataList = np.unique(list(itertools.chain.from_iterable(_list)))
        # 全データにナンバリング
        _flatDataNumberList = list(range(len(_flatDataList)))
        _numberKeyDict = {key: value for key, value in zip(_flatDataNumberList, _flatDataList)}
        _columnKeyDict = {key: value for value, key in _numberKeyDict.items()}
        return _numberKeyDict, _columnKeyDict


    @staticmethod
    def _encode(_list, _columnKeyDict) -> list:
        # orange3-associate用のデータ整形
        # 全データを番号に置換
        _encodedList = [
            [_columnKeyDict[column] for column in _each] for _each in _list
        ]
        return _encodedList


    @staticmethod
    def _decode(_X, _numberKeyDict) -> list:
        _result = []
        for number in _X:
            _idStrings = _numberKeyDict[number]
            _convertedDataDict = Pyfpgrowth._converteDictFromIdString(_idStrings)
            _result.append(_convertedDataDict)

        return _result


    @staticmethod
    def _removeStoreData(_list) -> list:
        result = []
        for _eachBasket in _list:
            for _each in _eachBasket:
                if (_each.startswith('store__')): # store__{"id": xxx}
                    _eachBasket.remove(_each)
            result.append(_eachBasket)
        return result


    @staticmethod
    def _removeMemberData(_list) -> list:
        result = []
        for _eachBasket in _list:
            for _each in _eachBasket:
                if (_each.startswith('member__')): # store__{"id": xxx}
                    _eachBasket.remove(_each)
            result.append(_eachBasket)
        return result

    @staticmethod
    def _removeSexData(_list) -> list:
        result = []
        for _eachBasket in _list:
            _eachResult = []
            for _each in _eachBasket:
                if not (_each.startswith('customerSex__')): # store__{"id": xxx}
                    _eachResult.append(_each)
            result.append(_eachResult)
        return result


    @staticmethod
    def createByPatternJson(_json):
        _loadedList = ujson.loads(_json)
        _patterns = {}
        for _eachDict, val in _loadedList.items():
            _patterns[ast.literal_eval(_eachDict)] = val

        return Pyfpgrowth(_patterns)


    @property
    def result(self):
        return self._result

    @property
    def patterns(self):
        return self._patterns


    @property
    def stringPatterns(self):
        return ujson.dumps(self._patterns)


    @property
    def rules(self):
        return 


    @property
    def stringRules(self):
        return ujson.dumps(self.rules)


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
        # rule作成の前にあらかじめ確認しないデータを省く必要がある？

        edges = []
        nodes = []

        if len(self._result) <= 0:
            return {"nodes": nodes, "edges": edges}

        _maxLift = max([nodeGroup['lift'] for nodeGroup in self._result])
        for nodeGroup in self._result:
            # edgesがlimitを超えたら了
            if (len(edges) > self.MAX_EDGE_COUNT): break

            # edgeから見ていく（キーの要素数が1、要素の要素数が1の場合）
            # edgeのfrom, toで、まだnodeにない場合はnodeに格納
            for node in nodeGroup['from']:
                nodeFrom = node
                if (nodeFrom["id"] not in [node["id"] for node in nodes]):
                    node = {
                        "id": nodeFrom["id"],
                        "label": nodeFrom["label"],
                        "value": 1,
                        "uri": "/",
                        "color": "#B69E86",
                    }
                    nodes.append(node)
            for node in nodeGroup['to']:
                nodeTo = node
                if (nodeTo["id"] not in [node["id"] for node in nodes]):
                    node = {
                        "id": nodeTo["id"],
                        "label": nodeTo["label"],
                        "value": 1,
                        "color": "#B69E86",
                    }
                    nodes.append(node)
            
            if (len(nodeGroup['from']) == 1) and (len(nodeGroup['to']) == 1):
                edge = {
                    "from": nodeGroup['from'][0]["id"],
                    "to": nodeGroup['to'][0]["id"],
                    "width": nodeGroup['lift'] / _maxLift * 5,
                    # "width": nodeGroup['confidence'],
                    "arrows": "to",
                }
                edges.append(edge)

        return {"nodes": nodes, "edges": edges}


    def _getDictForVis(self, data):
        if (data.startswith('product__')):
            dataJson = data.split('product__')[1]
            dataDict = ujson.loads(dataJson)
            return {
                "id":dataDict["id"],
                "label": self._productsApi.getProductById(dataDict["id"])["productName"]
            }
        # elif (data.startswith('customerSex__')): # product__{"id": xxx, "name": xxx, "categoryId": xxx}
        #     customerSexJson = data.split('customerSex__')[1]
        #     customerSexDict = ujson.loads(customerSexJson)
        #     nodeId = customerSexDict['sex']
        #     nodeLabel = customerSexDict['sex']

        #     return {
        #         "id"   : nodeId,
        #         "label": nodeLabel,
        #     }
        # elif (data.startswith('store__')): # product__{"id": xxx, "name": xxx, "categoryId": xxx}
        #     storeJson = data.split('store__')[1]
        #     storeDict = ujson.loads(storeJson)
        #     nodeId = storeDict["id"]
        #     nodeLabel = storeDict["id"]

        #     return {
        #         "id"   : nodeId,
        #         "label": nodeLabel,
        #     }
        # elif (data.startswith('member__')): # product__{"id": xxx, "name": xxx, "categoryId": xxx}
        #     memberJson = data.split('member__')[1]
        #     memberDict = ujson.loads(memberJson)
        #     nodeId = memberDict["id"]
        #     nodeLabel = memberDict["id"]

        #     return {
        #         "id"   : nodeId,
        #         "label": nodeLabel,
        #     }
        else:
            return None


    @staticmethod
    def _converteDictFromIdString(data) -> dict:
        _productsRepository = ProductsRepository()
        if (data.startswith('product__')):
            dataJson = data.split('product__')[1]
            dataDict = ujson.loads(dataJson)
            return {
                "id":dataDict["id"],
                "label": _productsRepository.getProductById(dataDict["id"]).name
            }
        elif (data.startswith('customerSex__')): # product__{"id": xxx, "name": xxx, "categoryId": xxx}
            customerSexJson = data.split('customerSex__')[1]
            customerSexDict = ujson.loads(customerSexJson)
            nodeId = customerSexDict['sex']
            nodeLabel = customerSexDict['sex']

            return {
                "id"   : nodeId,
                "label": nodeLabel,
            }
        elif (data.startswith('store__')): # product__{"id": xxx, "name": xxx, "categoryId": xxx}
            storeJson = data.split('store__')[1]
            storeDict = ujson.loads(storeJson)
            nodeId = storeDict["id"]
            nodeLabel = storeDict["id"]

            return {
                "id"   : nodeId,
                "label": nodeLabel,
            }
        elif (data.startswith('member__')): # product__{"id": xxx, "name": xxx, "categoryId": xxx}
            memberJson = data.split('member__')[1]
            memberDict = ujson.loads(memberJson)
            nodeId = memberDict["id"]
            nodeLabel = memberDict["id"]

            return {
                "id"   : nodeId,
                "label": nodeLabel,
            }
        else:
            return None