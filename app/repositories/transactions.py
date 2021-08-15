from typing import TypeVar, Type, List

import smaregipy

from app.entities.Transactions import Transaction, TransactionHead
from app.common.utils import EntityUtil

T = TypeVar('T', bound='TransactionsRepository')


class TransactionsRepository:

    @classmethod
    async def get_by_id(
        cls: Type[T],
        head_id: int,
        with_: List[str]
    ) -> Transaction:

        response = await (
            smaregipy.pos.Transaction()
            .id(head_id)
            .fetch()
        )
        return Transaction(
            response,
            response.details.__root__
        )

    @classmethod
    async def get_head_list_by_id_range(
        cls: Type[T],
        head_id_from: int,
        head_id_to: int
    ) -> List[TransactionHead]:
        """APIから取引ヘッダリストを取得します

        Args:
            headIdFrom (int): [description]
            headIdTo (int): [description]

        Returns:
            dict: 取引ヘッダID: [ヘッダリスト] の辞書
        """
        where_dict = {
            'transaction_head_id-from': head_id_from,
            'transaction_head_id-to': head_id_to,
        }

        head_list = (
            await smaregipy
            .pos
            .TransactionCollection()
            .fetch_all(**where_dict)
        )
        return [
            TransactionHead(**transaction.dict()) for transaction in head_list
        ]
