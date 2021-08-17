import dataclasses


@dataclasses.dataclass
class TransactionHead():
    def __init__(self, head: dict):
        self.transaction_head_id = head.get('transactionHeadId')
        self.transaction_date_time = head.get('transactionDateTime')
        self.transaction_head_division = head.get('transactionHeadDivision')
        self.cancel_division = head.get('cancelDivision')
        self.unit_non_discountsubtotal = head.get('unitNonDiscountsubtotal')
        self.unit_discountsubtotal = head.get('unitDiscountsubtotal')
        self.unit_staff_discountsubtotal = head.get(
            'unitStaffDiscountsubtotal'
        )
        self.unit_bargain_discountsubtotal = head.get(
            'unitBargainDiscountsubtotal'
        )
        self.subtotal = head.get('subtotal')
        self.subtotal_for_discount = head.get('subtotalForDiscount')
        self.subtotal_discount_price = head.get('subtotalDiscountPrice')
        self.subtotal_discount_rate = head.get('subtotalDiscountRate')
        self.subtotal_discount_division = head.get('subtotalDiscountDivision')
        self.point_discount = head.get('pointDiscount')
        self.coupon_discount = head.get('couponDiscount')
        self.total = head.get('total')
        self.tax_include = head.get('taxInclude')
        self.tax_exclude = head.get('taxExclude')
        self.rounding_division = head.get('roundingDivision')
        self.rounding_price = head.get('roundingPrice')
        self.cash_total = head.get('cashTotal')
        self.credit_total = head.get('creditTotal')
        self.deposit = head.get('deposit')
        self.deposit_cash = head.get('depositCash')
        self.deposit_credit = head.get('depositCredit')
        self.change = head.get('change')
        self.tip_cash = head.get('tipCash')
        self.tip_credit = head.get('tipCredit')
        self.amount = head.get('amount')
        self.return_amount = head.get('returnAmount')
        self.cost_total = head.get('costTotal')
        self.sales_head_division = head.get('salesHeadDivision')
        self.in_tax_sales_total = head.get('inTaxSalesTotal')
        self.out_tax_sales_total = head.get('outTaxSalesTotal')
        self.non_tax_sales_total = head.get('nonTaxSalesTotal')
        self.non_sales_target_total = head.get('nonSalesTargetTotal')
        self.non_sales_target_out_tax_total = head.get(
            'nonSalesTargetOutTaxTotal'
        )
        self.non_sales_target_in_tax_total = head.get(
            'nonSalesTargetInTaxTotal'
        )
        self.non_sales_target_tax_free_total = head.get(
            'nonSalesTargetTaxFreeTotal'
        )
        self.non_sales_target_cost_total = head.get('nonSalesTargetCostTotal')
        self.non_sales_target_amount = head.get('nonSalesTargetAmount')
        self.non_sales_target_return_amount = head.get(
            'nonSalesTargetReturnAmount'
        )
        self.new_point = head.get('newPoint')
        self.spend_point = head.get('spendPoint')
        self.point = head.get('point')
        self.total_point = head.get('totalPoint')
        self.current_mile = head.get('currentMile')
        self.earn_mile = head.get('earnMile')
        self.total_mile = head.get('totalMile')
        self.adjustment_mile = head.get('adjustmentMile')
        self.adjustment_mile_division = head.get('adjustmentMileDivision')
        self.adjustment_mile_value = head.get('adjustmentMileValue')
        self.store_id = head.get('storeId')
        self.store_code = head.get('storeCode')
        self.terminal_id = head.get('terminalId')
        self.customer_id = head.get('customerId')
        self.customer_code = head.get('customerCode')
        self.terminal_tran_id = head.get('terminalTranId')
        self.terminal_tran_date_time = head.get('terminalTranDateTime')
        self.sum_division = head.get('sumDivision')
        self.adjustment_date_time = head.get('adjustmentDateTime')
        self.sum_date = head.get('sumDate')
        self.customer_rank = head.get('customerRank')
        self.customer_group_id = head.get('customerGroupId')
        self.customer_group_id2 = head.get('customerGroupId2')
        self.customer_group_id3 = head.get('customerGroupId3')
        self.customer_group_id4 = head.get('customerGroupId4')
        self.customer_group_id5 = head.get('customerGroupId5')
        self.staff_id = head.get('staffId')
        self.staff_code = head.get('staffCode')
        self.staff_name = head.get('staffName')
        self.credit_division = head.get('creditDivision')
        self.payment_count = head.get('paymentCount')
        self.slip_number = head.get('slipNumber')
        self.cancel_slip_number = head.get('cancelSlipNumber')
        self.auth_number = head.get('authNumber')
        self.auth_date = head.get('authDate')
        self.card_company = head.get('cardCompany')
        self.denomination = head.get('denomination')
        self.memo = head.get('memo')
        self.receipt_memo = head.get('receiptMemo')
        self.carriage = head.get('carriage')
        self.commission = head.get('commission')
        self.guest_numbers = head.get('guestNumbers')
        self.guest_numbers_male = head.get('guestNumbersMale')
        self.guest_numbers_female = head.get('guestNumbersFemale')
        self.guest_numbers_unknown = head.get('guestNumbersUnknown')
        self.enter_date_time = head.get('enterDateTime')
        self.tax_free_sales_division = head.get('taxFreeSalesDivision')
        self.net_tax_free_general_tax_include = head.get(
            'netTaxFreeGeneralTaxInclude'
        )
        self.net_tax_free_general_tax_exclude = head.get(
            'netTaxFreeGeneralTaxExclude'
        )
        self.net_tax_free_consumable_tax_include = head.get(
            'netTaxFreeConsumableTaxInclude'
        )
        self.net_tax_free_consumable_tax_exclude = head.get(
            'netTaxFreeConsumableTaxExclude'
        )
        self.tags = head.get('tags')
        self.point_giving_division = head.get('pointGivingDivision')
        self.point_giving_unit_price = head.get('pointGivingUnitPrice')
        self.point_giving_unit = head.get('pointGivingUnit')
        self.point_spend_division = head.get('pointSpendDivision')
        self.mileage_division = head.get('mileageDivision')
        self.mileage_label = head.get('mileageLabel')
        self.customer_pin_code = head.get('customerPinCode')
        self.return_sales = head.get('returnSales')
        self.dispose_division = head.get('disposeDivision')
        self.dispose_server_transaction_head_id = head.get(
            'disposeServerTransactionHeadId'
        )
        self.cancel_date_time = head.get('cancelDateTime')
        self.sell_division = head.get('sellDivision')
        self.tax_rate = head.get('taxRate')
        self.tax_rounding = head.get('taxRounding')
        self.discount_rounding_division = head.get('discountRoundingDivision')
        self.transaction_uuid = head.get('transactionUuid')
        self.exchange_ticket_no = head.get('exchangeTicketNo')
        self.gift_receipt_valid_days = head.get('giftReceiptValidDays')
        self.barcode = head.get('barcode')
        self.upd_date_time = head.get('updDateTime')


@dataclasses.dataclass
class TransactionDetail():
    def __init__(self, detail: dict):
        # dict.get()は存在しないキーの場合Noneを返す
        self.transaction_head_id = detail.get("transactionHeadId")

        self.transaction_detail_id = detail.get("transactionDetailId")
        self.parent_transaction_detail_id = detail.get(
            "parentTransactionDetailId"
        )
        self.transaction_detail_division = detail.get(
            "transactionDetailDivision"
        )
        self.product_id = detail.get("productId")
        self.product_code = detail.get("productCode")
        self.product_name = detail.get("productName")
        self.print_receipt_product_name = detail.get("printReceiptProductName")
        self.color = detail.get("color")
        self.size = detail.get("size")
        self.group_code = detail.get("groupCode")
        self.tax_division = detail.get("taxDivision")
        self.price = detail.get("price")
        self.sales_price = detail.get("salesPrice")
        self.unit_discount_price = detail.get("unitDiscountPrice")
        self.unit_discount_rate = detail.get("unitDiscountRate")
        self.unit_discount_division = detail.get("unitDiscountDivision")
        self.cost = detail.get("cost")
        self.quantity = detail.get("quantity")
        self.unit_non_discount_sum = detail.get("unitNonDiscountSum")
        self.unit_discount_sum = detail.get("unitDiscountSum")
        self.unit_discounted_sum = detail.get("unitDiscountedSum")
        self.costSum = detail.get("costSum")
        self.category_id = detail.get("categoryId")
        self.category_name = detail.get("categoryName")
        self.discrimination_no = detail.get("discriminationNo")
        self.sales_division = detail.get("salesDivision")
        self.product_division = detail.get("product")
        self.inventory_reservation_division = detail.get(
            "inventoryReservationDivision"
        )
        self.point_not_applicable = detail.get("pointNotApplicable")
        self.calc_discount = detail.get("calcDiscount")
        self.tax_free_division = detail.get("taxFreeDivision")
        self.tax_free_commodity_price = detail.get("taxFreeCommodityPrice")
        self.tax_free = detail.get("taxFree")
        self.product_bundle_group_id = detail.get("productBundleGroupId")
        self.discount_price_proportional = detail.get(
            "discountPriceProportional"
        )
        self.discount_point_proportional = detail.get(
            "discountPointProportional"
        )
        self.discount_coupon_proportional = detail.get(
            "discountCouponProportional"
        )
        self.tax_include_proportional = detail.get("taxIncludeProportional")
        self.tax_exclude_proportional = detail.get("taxExcludeProportional")
        self.product_bundle_proportional = detail.get(
            "productBundleProportional"
        )
        self.staff_discount_proportional = detail.get(
            "staffDiscountProportional"
        )
        self.bargain_discount_proportional = detail.get(
            "bargainDiscountProportional"
        )
        self.rounding_price_proportional = detail.get(
            "roundingPriceProportional"
        )
        self.product_staff_discountRate = detail.get("productStaffDiscountRate")
        self.staff_rank = detail.get("staffRank")
        self.staff_rank_name = detail.get("staffRankName")
        self.staff_discount_rate = detail.get("staffDiscountRate")
        self.staff_discount_division = detail.get("staffDiscountDivision")
        self.apply_staff_discount_rate = detail.get("applyStaffDiscountRate")
        self.apply_staff_discount_price = detail.get("applyStaffDiscountPrice")
        self.bargain_id = detail.get("bargainId")
        self.bargain_name = detail.get("bargainName")
        self.bargain_division = detail.get("bargainDivision")
        self.bargain_value = detail.get("bargainValue")
        self.apply_bargain_value = detail.get("applyBargainValue")
        self.apply_bargain_discount_price = detail.get(
            "applyBargainDiscountPrice"
        )
        self.tax_rate = detail.get("taxRate")
        self.standard_tax_rate = detail.get("standardTaxRate")
        self.modified_tax_rate = detail.get("modifiedTaxRate")
        self.reduce_tax_id = detail.get("reduceTaxId")
        self.reduce_tax_name = detail.get("reduceTaxName")
        self.reduce_tax_rate = detail.get("reduceTaxRate")
        self.reduce_tax_price = detail.get("reduceTaxPrice")
        self.reduce_tax_member_price = detail.get("reduceTaxMemberPrice")
