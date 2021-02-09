from ..BaseServiceApi import BaseServiceApi


class TransactionsApi(BaseServiceApi):
    def __init__(self, config):
        super().__init__(config)


    def getTransactionHeadList(self, field=None, sort=None, whereDict=None):
        contractId = self.config.contractId
        self.uriPos = self.config.uriApi + '/' + contractId + '/pos'
        self.uri = self.uriPos + '/transactions'
        
        header = self._getHeader()
        body = self._getBody(sort=sort, whereDict=whereDict)
        
        result = self._api(self.uri, header, body)
        return result


    def getTransactionDetail(self,transactionHeadId, field=None, sort=None, whereDict=None):
        contractId = self.config.contractId
        self.uriPos = self.config.uriApi + '/' + contractId + '/pos'
        self.uri = self.uriPos + '/transactions/' + transactionHeadId + '/details'
        
        header = self._getHeader()
        body = self._getBody(sort=sort, whereDict=whereDict)
        
        result = self._api(self.uri, header, body)
        return result
        

    def getTransaction(self,transactionHeadId, field=None, sort=None, whereDict=None):
        contractId = self.config.contractId
        self.uriPos = self.config.uriApi + '/' + contractId + '/pos'
        self.uri = self.uriPos + '/transactions/' + transactionHeadId
        
        header = self._getHeader()
        body = self._getBodyForDetail(sort=sort, whereDict=whereDict)
        
        result = self._api(self.uri, header, body)
        return result
        
        
class TransactionDetail():
    def __init__(self):
        self._transactionHeadId = None 
        self._transactionDetailId = None 
        self._parentTransactionDetailId = None 
        self._transactionDetailDivision = None 
        self._productId = None 
        self._productCode = None 
        self._productName = None 
        self._printReceiptProductName = None 
        self._color = None 
        self._size = None 
        self._groupCode = None 
        self._taxDivision = None 
        self._price = None 
        self._salesPrice = None 
        self._unitDiscountPrice = None 
        self._unitDiscountRate = None 
        self._unitDiscountDivision = None 
        self._cost = None 
        self._quantity = None 
        self._unitNonDiscountSum = None 
        self._unitDiscountSum = None 
        self._unitDiscountedSum = None 
        self._costSum = None 
        self._categoryId = None 
        self._categoryName = None 
        self._discriminationNo = None 
        self._salesDivision = None 
        self._productDivision = None 
        self._inventoryReservationDivision = None 
        self._pointNotApplicable = None 
        self._calcDiscount = None 
        self._taxFreeDivision = None 
        self._taxFreeCommodityPrice = None 
        self._taxFree = None 
        self._productBundleGroupId = None 
        self._discountPriceProportional = None 
        self._discountPointProportional = None 
        self._discountCouponProportional = None 
        self._taxIncludeProportional = None 
        self._taxExcludeProportional = None 
        self._productBundleProportional = None 
        self._staffDiscountProportional = None 
        self._bargainDiscountProportional = None 
        self._roundingPriceProportional = None 
        self._productStaffDiscountRate = None 
        self._staffRank = None 
        self._staffRankName = None 
        self._staffDiscountRate = None 
        self._staffDiscountDivision = None 
        self._applyStaffDiscountRate = None 
        self._applyStaffDiscountPrice = None 
        self._bargainId = None 
        self._bargainName = None 
        self._bargainDivision = None 
        self._bargainValue = None 
        self._applyBargainValue = None 
        self._applyBargainDiscountPrice = None 
        self._taxRate = None 
        self._standardTaxRate = None 
        self._modifiedTaxRate = None 
        self._reduceTaxId = None 
        self._reduceTaxName = None 
        self._reduceTaxRate = None 
        self._reduceTaxPrice = None 
        self._reduceTaxMemberPrice = None

