import pyfpgrowth

class Basket():
    def __init__(self):
        self._inputData = []
        self._output = {}
        self._products = {}
        
        
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
        
                
    def analyze(self):
        patterns = pyfpgrowth.find_frequent_patterns(self._inputData, 2)
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
    
    
    @property
    def result(self):
        return self._output
        
        
    def salesRanking(self, top=1):
        nodes = self._output['nodes']
        print('nodes : ')
        print (nodes)
        sortedProductIdList = sorted(nodes, key=lambda x: x['value'], reverse=True)
        print (sortedProductIdList)
        print (sortedProductIdList[0: top])

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