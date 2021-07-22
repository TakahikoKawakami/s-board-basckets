from typing import TypeVar, Type, List

import smaregipy

from app.entities.Transactions import Transaction

T = TypeVar('T', bound='TransactionsRepository')


class TransactionsRepository:

    @classmethod
    async def get_by_id(
        cls: Type[T],
        head_id: int,
        with_: List[str]
    ) -> Transaction:
        where_dict = {}
        if 'details' in with_:
            where_dict['with_details'] = 'all'

        response = await smaregipy.pos.Transaction()\
            .id(head_id)\
            .get(**where_dict)
        return Transaction(
            response,
            response.details.records.values()
        )

