from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, ValidationError
from wtforms.fields.html5 import DateField
from wtforms.validators import Required, Length

class BasketForm(FlaskForm):
    storeField = SelectField( "分析する店舗は？",
        choices = [ ],
        validators = [
            Required(u"分析する店舗を選択してください"),
        ]
    )
    dateFromField = DateField("いつから分析する？",
        validators = [
            Required(u"分析を開始する日付を選択してください"),
        ]
    )
    dateToField = DateField("いつまで分析する？",
        validators = [
            Required(u"分析を終了する日付を選択してください"),
        ]
    )

    def validate_storeField(self, storeField):
        """validation for store

        Arguments:
            storeField {[type]} -- [description]
        """
        if storeField.data == "":
            raise ValidationError("店舗を指定してください")


    def validate_dateFromField(self, dateFromField):
        if dateFromField.data == "":
            raise ValidationError("開始日を選択してください")


    def validate_dateToField(self, dateToField):
        if dateToField.data == "":
            raise ValidationError("終了日を選択してください")
        

    def setStoreList(self, _setStoreList) -> None:
        _choices = []
        for _store in _setStoreList:
            _tuple = (_store["storeId"], _store["storeName"])
            _choices.append(_tuple)

        self.storeField.choices = _choices