from typing import TypeVar, Type

import smaregipy


T = TypeVar('T', bound='CustomerGroupsRepository')


class CustomerGroupsRepository:

    @classmethod
    async def get_by_id(
        cls: Type[T],
        customer_group_id: int
    ) -> smaregipy.pos.CustomerGroup:
        """
            2021-08-187現在、客層は一覧取得のみなので、そちらから取得する
        """

        customer_group_list = await (
            smaregipy
            .pos
            .CustomerGroupCollection()
            .fetch_all()
        )
        
        return customer_group_list.find(customer_group_id)
