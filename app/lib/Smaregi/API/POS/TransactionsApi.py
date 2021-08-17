from ..BaseServiceApi import BaseServiceApi
from .entities import TransactionHead, TransactionDetail


class TransactionsApi(BaseServiceApi):
    def __init__(self, config):
        super().__init__(config)


    def getTransactionHeadList(self, field=None, sort=None, whereDict=None) -> TransactionHead:
        contractId = self.config.contractId
        self.uriPos = self.config.uriApi + '/' + contractId + '/pos'
        self.uri = self.uriPos + '/transactions'
        
        header = self._getHeader()
        body = self._getQuery(sort=sort, whereDict=whereDict)
        
        response = self._apiGet(self.uri, header, body)
        if response[0] != 200:
            raise Exception(response[1])
        responseData = response[1]
        result = [TransactionHead(data) for data in responseData]
        return result


    def getTransactionDetail(self,transactionHeadId, field=None, sort=None, whereDict=None) -> list['TransactionDetail']:
        contractId = self.config.contractId
        self.uriPos = self.config.uriApi + '/' + contractId + '/pos'
        self.uri = self.uriPos + '/transactions/' + transactionHeadId + '/details'
        
        header = self._getHeader()
        body = self._getQuery(sort=sort, whereDict=whereDict)
        
        response = self._apiGet(self.uri, header, body)
        if response[0] != 200:
            raise Exception(response[1])
        responseData = response[1]
        result = [TransactionDetail(data) for data in responseData]
        return result
        

    def getTransaction(self,transactionHeadId, field=None, sort=None, whereDict=None) -> dict[str, 'TransactionHead' or 'TransactionDetail']:
        """取引取得APIを実施します

        Returns:
            dict: head, detailsをキーに持つdict型。各々の要素はTransactionHead、TransactionDetail型
        """
        contractId = self.config.contractId
        self.uriPos = self.config.uriApi + '/' + contractId + '/pos'
        self.uri = self.uriPos + '/transactions/' + transactionHeadId
        
        header = self._getHeader()
        body = self._getQueryForDetail(sort=sort, whereDict=whereDict)
        
        response = self._apiGet(self.uri, header, body)
        if response[0] != 200:
            raise Exception(response[1])
        responseData = response[1]
        result = {}
        result["head"] = TransactionHead(responseData)
        if response.get("details") is not None:
            result["details"] = [TransactionDetail(data) for data in responseData.get("details")]
        return result
        
    
    def createTransactionDetailCsv(self, field=None, sort=None, whereDict=None):
        """取引明細CSV作成APIを実施します

        Args:
            field (dict, optional): [description]. Defaults to None.
            sort (dict, optional): [description]. Defaults to None.
            whereDict (dict, optional): [description]. Defaults to None.
        """
        contractId = self.config.contractId
        self.uriPos = self.config.uriApi + '/' + contractId + '/pos'
        self.uri = self.uriPos + '/transactions/details/out_file_async'
        
        header = self._getHeader()

        body = self._getQueryForDetail(sort=sort, whereDict=whereDict, state={
            'contractId': self.config.contractId,
            'field': field,
            'sort': sort,
            'where': whereDict,
        })
        
        response = self._apiPost(self.uri, header, body)
        if response[0] != 200:
            raise Exception(response[1])
        responseData = response[1]
        return responseData
