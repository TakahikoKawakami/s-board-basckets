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


class BasketForm(Form):
    storeField = SelectField( "分析する店舗は？",
        choices = [ ],
        validators = [
            Required(u"分析する店舗を選択してください"),
        ]
    )
    dateFromField = DateField("いつから分析する？",
        validators = [
            Required(u"分析を開始する日付を選択してください"),
        ],
        default = datetime.datetime.today() - relativedelta(days=1),
        format = "%Y-%m-%d"
    )
    dateToField = DateField("いつまで分析する？",
        validators = [
            Required(u"分析を終了する日付を選択してください"),
        ],
        default = datetime.datetime.today() - relativedelta(days=1),
        format = "%Y-%m-%d"
    )

    def validate_storeField(self, storeField):
        """validation for store

        Arguments:
            storeField {[type]} -- [description]
        """
        if storeField.data == "":
            raise ValidationError("[店舗] 店舗を指定してください")


    def validate_dateFromField(self, dateFromField):
        if type(dateFromField.data) is datetime.datetime:
            dateFromField.data = dateFromField.data.date()
        if type(self.dateToField.data) is datetime.datetime:
            self.dateToField.data = self.dateToField.data.date()
        _today = datetime.date.today()
        if (dateFromField.data >= _today):
            raise ValidationError("[開始日] 指定できる日付は昨日までです")
        if (dateFromField.data > self.dateToField.data):
            raise ValidationError("[開始日][終了日] 日付の大小関係が不正です")
        if (self.dateToField.data - dateFromField.data).days > 90:
            raise ValidationError("[開始日][終了日] 分析できる期間は90日です")


    def validate_dateToField(self, dateToField):
        if type(dateToField.data) is datetime.datetime:
            dateToField.data = dateToField.data.date()
        _today = datetime.date.today()
        if (dateToField.data >= _today):
            raise ValidationError("[終了日] 指定できる日付は昨日までです")
        

    def setStoreList(self, _setStoreList) -> None:
        _choices = []
        for _store in _setStoreList:
            _tuple = (_store["storeId"], _store["storeName"])
            _choices.append(_tuple)

        self.storeField.choices = _choices