from sqlalchemy import Column, Integer, Unicode, UnicodeText, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship, backref
from datetime import datetime

from database import db

import pyfpgrowth
import logging

class Basket(db.Model):
    """
    買い物かごモデル
    """
    __tablename__ = "baskets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Unicode(32), nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    analyze_result = Column(Integer, nullable=False)


    created_at = Column(DateTime)
    modified_at = Column(DateTime)


    def __init__(self):
        self._inputData = []
        self._output = {}
        self._products = {}
        self._logger = logging.getLogger('flask.app')
        
        
    def __resp__(self):
        pass
        
        
    def __str__(self):
        return \
            "input: " + self._inputData + "\n" + \
            "output: " + self._output


    def append(self, transactionDetailList):
        result = []
        for transactionDetail in transactionDetailList:
            result.append(
                transactionDetail['productId']
            )
            self._products[transactionDetail['productId']] = \
                transactionDetail['productName']
            

        self._inputData.append(result)

        return self
        
                
    def analyze(self, rate=1):
        targetCount = len(self._inputData) * rate / 100.0
        patterns = pyfpgrowth.find_frequent_patterns(self._inputData, targetCount)
        self._logger.info(patterns)
        edges = []
        nodes = []
        for k,v in patterns.items():
            if (len(k) == 1):
                print(k)
                productId = k[0]
                nodes.append({
                    "id": productId,
                    "label": self._products[productId],
                    "value": v
                })
            elif (len(k) == 2):
                edges.append({
                    "from": k[0],
                    "to": k[1],
                    "value": v
                })
    
        self._output['nodes'] = nodes
        self._output['edges'] = edges
        
        return self
    

    def resultByProductId(self, productId):
        edges = self._output['edges']
        targetEdges = []
        for edge in edges:
            if (productId == edge["from"]):
                targetEdges.append({
                    "target": edge["to"],
                    "value": edge["value"]
                })
            elif (productId == edge["to"]):
                targetEdges.append({
                    "target": edge["from"],
                    "value": edge["value"]
                })
        self._logger.info(targetEdges)
        return targetEdges

    
    @property
    def result(self):
        return self._output
        
        
    def salesRanking(self, top=0):
        nodes = self._output['nodes']
        sortedNodesByProductIdList = sorted(nodes, key=lambda x: x['value'], reverse=True)
        targetNodes = sortedNodesByProductIdList[0: top]
        result = []
        for node in targetNodes:
            self._logger.info(node['id'])
            newNode = node['relations'] = self.relationRanking(node['id'])
            result.append(node)
        self._logger.info(result)
        return result


    def relationRanking(self, productId, top=1):
        nodes = self.resultByProductId(productId)
        sortedProductIdList = sorted(nodes, key=lambda x: x['value'], reverse=True)

        return sortedProductIdList[0: top]

    
# result = bascket().append(inputData).analyze().result

class MockBasket():
    def append(self, transactionDetailList):
        pass


    def analyze(self):
        return self


    @property
    def result(self):
        return {
            'nodes': [
                {
                    'id': 'product_1',
                    "label": 'product_1',
                    "value": 1,
                },
                {
                    'id': 'product_2',
                    "label": 'product_2',
                    "value": 1,
                },
                {
                    'id': 'product_3',
                    "label": 'product_3',
                    "value": 3,
                },
            ],
            'edges': [
                {
                    "from": 'product_1',
                    "to": 'product_2',
                    "value": 1
                },
                {
                    "from": 'product_1',
                    "to": 'product_3',
                    "value": 3
                }
            ]
        }

    
    def salesRanking(self, top=1):
        pass