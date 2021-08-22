from typing import TypeVar, Type, List

import smaregipy

from app.entities.Transactions import Transaction
from app.common.utils import EntityUtil

T = TypeVar('T', bound='ProductsRepository')


class ProductsRepository:

    @classmethod
    async def get_by_id(
        cls: Type[T],
        product_id: int
    ) -> smaregipy.pos.Product:

        return await smaregipy.pos.Product().id(product_id).fetch()
