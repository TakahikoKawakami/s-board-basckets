from ..BaseServiceApi import BaseServiceApi


class StoresApi(BaseServiceApi):
    def __init__(self, config):
        super().__init__(config)


    def __repr__(self):
        # return '<{}, {}, {}>".format(self.id, self.)"'
        pass


    def getStoreList(self, field=None, sort=None, whereDict=None):
        contractId = self.config.contractId
        self.uriPos = self.config.uriApi + '/' + contractId + '/pos'
        self.uri = self.uriPos + '/stores'
        
        header = self._getHeader()
        body = self._getQuery('storeId,storeName', sort, whereDict)
        
        response = self._apiGet(self.uri, header, body)
        if response[0] != 200:
            raise response[1]
        responseData = response[1]

        return responseData


    def getStoreById(self, id, ield=None, sort=None, whereDict=None):
        contractId = self.config.contractId
        self.uriPos = self.config.uriApi + '/' + contractId + '/pos'
        self.uri = self.uriPos + '/stores/' + id
        
        header = self._getHeader()
        body = self._getQueryForDetail('storeId,storeName', sort, whereDict)
        
        response = self._apiGet(self.uri, header, body)
        if response[0] != 200:
            raise response[1]
        responseData = response[1]
        return responseData

