from tortoise import fields

from app.common.abstracts.AbstractTortoiseModel import AbstractTortoiseModel


class CallbackQuery(AbstractTortoiseModel):
    """
    コールバックのクエリ
    コールバックされたデータが何の検索結果かを保存するためのモデル
    """
    query = fields.TextField(null=True, default=[])

    class Meta:
        abstract = False
        table = "callback_query"


