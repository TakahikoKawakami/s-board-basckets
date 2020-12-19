from flask import redirect


from ..BaseServiceApi import BaseServiceApi


class StoresApi(BaseServiceApi):
    def __init__(self, config):
        super().__init__(config)


    def getStoreList(self, field=None, sort=None, whereDict=None):
        contractId = self.config.contractId
        self.uriPos = self.config.uriApi + '/' + contractId + '/pos'
        self.uri = self.uriPos + '/stores'
        
        header = self._getHeader()
        body = self._getBody('storeId,storeName', sort, whereDict)
        
        result = self._api(self.uri, header, body)
        return result
