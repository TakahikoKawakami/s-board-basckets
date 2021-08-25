from typing import List, Type, TypeVar
from datetime import date

from app.entities.notifications import Notification, NotificationId

T = TypeVar('T', bound='NotificationRepository')

all_notifications = [
    Notification(
        notification_id=NotificationId.parse_obj(0),
        summary='test1',
        detail="""
            <b>test bold</b>
        """,
        timestamp=date(2021, 8, 25)
    ),
    Notification(
        notification_id=NotificationId.parse_obj(1),
        summary='test2',
        detail="""
            <p>paragraph</p>
        """,
        timestamp=date(2021, 8, 25)
    ),
    Notification(
        notification_id=NotificationId.parse_obj(2),
        summary='test3',
        detail="""
            <a href="https://google.com">google</a>
        """,
        timestamp=date(2021, 8, 25)
    )
]


class NotificationRepository:
    @classmethod
    def get_all(cls: Type[T]) -> List[Notification]:
        return all_notifications

    @classmethod
    def find(cls: Type[T], id_: int) -> Notification:
        return all_notifications[id_]
