import datetime
from dateutil.relativedelta import relativedelta

from marshmallow import Schema, fields, validates, validates_schema, ValidationError


class AccosiationCondition(Schema):
    store_id = fields.String(
        required=True,
        error_messages={"required": "[店舗選択] 設定画面から、店舗を選択してください"}
    )
    date_from = fields.Date(
        required=True,
        error_messages={"required": "[開始日] 開始日を選択してください"}
    )
    date_to = fields.Date(
        required=True,
        error_messages={"required": "[終了日] 終了日を選択してください"}
    )

    class Meta:
        strict = True

    @validates('date_from')
    def validate_dateFrom(self, value):
        if type(value) is datetime.datetime:
            value = value.date()
        _today = datetime.date.today()
        if (value > _today):
            raise ValidationError("[開始日] 指定できる日付は今日までです")

    @validates('date_to')
    def validate_dateTo(self, value):
        if type(value) is datetime.datetime:
            value = value.date()
        _today = datetime.date.today()
        if (value > _today):
            raise ValidationError("[終了日] 指定できる日付は今日までです")

    @validates_schema
    def validate_dateFromTo(self, data, **kwargs):
        if type(data['date_from']) is datetime.datetime:
            data['date_from'] = data['date_from'].date()
        if type(data['date_to']) is datetime.datetime:
            data['date_to'] = data['date_to'].date()

        if (data['date_from'] > data['date_to']):
            raise ValidationError("[開始日][終了日] 日付の大小関係が不正です")
        if (data['date_from'] - data['date_to']).days > 90:
            raise ValidationError("[開始日][終了日] 分析できる期間は90日です")
        
