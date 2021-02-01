import datetime
from dateutil.relativedelta import relativedelta

from wtforms import Form, SelectField, StringField, ValidationError
from wtforms.fields.html5 import DateField
from wtforms.validators import Required, Length

from marshmallow import Schema, fields

class AccosiationCondition(Schema):
    storeId = fields.Integer(required=True)
    dateFrom = fields.Date(required=True)
    dateTo = fields.Date(required=True)

    class Meta:
        strict = True

    @validators('dateFrom')
    def validate_dateFrom(self, value):
        if type(value.data) is datetime.datetime:
            value.data = value.data.date()
        if type(self.dateToField.data) is datetime.datetime:
            self.dateToField.data = self.dateToField.data.date()
        _today = datetime.date.today()
        if (value.data >= _today):
            raise ValidationError("[開始日] 指定できる日付は昨日までです")
        if (value.data > self.dateToField.data):
            raise ValidationError("[開始日][終了日] 日付の大小関係が不正です")
        if (self.dateToField.data - value.data).days > 90:
            raise ValidationError("[開始日][終了日] 分析できる期間は90日です")

    @validators('dateTo')
    def validate_dateTo(self, dateToField):
        if type(dateToField.data) is datetime.datetime:
            dateToField.data = dateToField.data.date()
        _today = datetime.date.today()
        if (dateToField.data >= _today):
            raise ValidationError("[終了日] 指定できる日付は昨日までです")

