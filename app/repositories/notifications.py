from typing import List, Type, TypeVar
from datetime import date

from app.entities.notifications import Notification, NotificationId

T = TypeVar('T', bound='NotificationRepository')

all_notifications = [
    Notification(
        notification_id=NotificationId.parse_obj(0),
        summary='ver 1.1.0バージョンアップのお知らせ',
        detail="""
            <p>ver 1.1.0へバージョンアップを行いました。</p>
            <p>追加された機能は下記のとおりです。</p>
            <hr>
            <ol>
                <li>
                    <h3>お知らせ機能</h3>
                    <p>
                        現在ご覧いただいているような、バージョンアップや不具合修正のお知らせを<br>
                        表示する機能を実装しました。
                    </p>
                </li>
                <li>
                    <h3>客層-商品分析機能</h3>
                    <p>
                        【客層-商品】間の関連性を分析できる機能を追加しました。<br>
                        【分析対象】のプルダウンメニューからお選びいただき、分析開始ボタンを押下いただくことで利用できます。
                    </p>
                </li>
                <li>
                    <h3>お知らせ機能</h3>
                    <p>現在ご覧いただいているような、バージョンアップや不具合修正のお知らせを<br>
                    表示する機能を実装しました。</p>
                </li>
                <li>
                    <h3>お知らせ機能</h3>
                    <p>現在ご覧いただいているような、バージョンアップや不具合修正のお知らせを<br>
                    表示する機能を実装しました。</p>
                </li>
            </ol>
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
