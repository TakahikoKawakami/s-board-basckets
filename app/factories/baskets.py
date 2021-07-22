from app.entities.Transactions import Transaction
from app.entities.Baskets import Basket


class BasketsFactory:
    @staticmethod
    def make_basket_by_transaction(transaction: Transaction) -> Basket:
        basket = Basket()
        basket.set_by_transaction_head(transaction.head)
        basket.set_by_transaction_detail_list(transaction.details)
        return basket
