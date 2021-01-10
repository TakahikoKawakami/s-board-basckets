from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, ValidationError
from wtforms.fields.html5 import DateField

class BasketForm(FlaskForm):
    storeField = SelectField( "店舗選択",
        choices = [ ]
    )
    dateFromField = DateField("開始日")
    dateToField = DateField("終了日")

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