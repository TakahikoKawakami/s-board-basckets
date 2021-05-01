from enum import Enum, IntEnum, auto
from tortoise import fields
from datetime import datetime

from app.common.abstracts.AbstractTortoiseModel import AbstractTortoiseModel
from app.entities.AccessToken import AccessToken


class AccountSetting(AbstractTortoiseModel):
    """
    アカウント設定モデル
    """
    display_store_id = fields.IntField(null=True)
    use_smaregi_webhook = fields.BooleanField(default=False)

    account: fields.ReverseRelation["Account"]

    class Meta:
        abstract=False
        table="account_setting"

    @property
    def displayStoreId(self):
        return self.display_store_id

    @displayStoreId.setter
    def displayStoreId(self, val):
        self.display_store_id = val

    @property
    def useSmaregiWebhook(self):
        return self.use_smaregi_webhook

    @useSmaregiWebhook.setter
    def useSmaregiWebhook(self, val):
        self.use_smaregi_webhook = val


class Account(AbstractTortoiseModel):
    """
    アカウントモデル
    """

    class Meta:
        abstract=False
        table="accounts"

    class PlanEnum(IntEnum):
        FREE = 0
        STANDARD = auto()
        PREMIUM = auto()

        @classmethod
        def getPlanName(cls, enum: int) -> str:
            """enum値からプラン名を返します

            Args:
                enum (int): [description]

            Returns:
                str: [description]
            """
            if enum == cls.FREE:
                return "フリープラン"
            if enum == cls.STANDARD:
                return "スタンダードプラン"
            if enum == cls.PREMIUM:
                return "プレミアムプラン"
            return None

        @classmethod
        def getPlanEnumValue(cls, planName: str) -> int:
            """プラン名からenum値を返します

            Args:
                planName (str): [description]

            Returns:
                int: [description]
            """
            if planName ==  "フリープラン":
                return cls.FREE
            elif planName == "スタンダードプラン":
                return cls.STANDARD
            elif planName == "プレミアムプラン":
                return cls.PREMIUM
            else:
                return cls.PREMIUM
            return None

    class StatusEnum(IntEnum):
        STATUS_START = 0
        STATUS_STOP = auto()

    class LoginStatusEnum(Enum):
        SIGN_UP = 0
        SIGN_IN = auto()
        SIGN_ON = auto()
        SIGN_OUT = auto()

    loginStatus = LoginStatusEnum.SIGN_ON

    access_token = fields.CharField(max_length = 1024)
    expiration_date_time = fields.DatetimeField()
    status = fields.CharField(max_length = 16, null = True)
    user_status = fields.IntEnumField(enum_type = StatusEnum)
    plan = fields.IntEnumField(enum_type = PlanEnum, null = True)
#    last_login_version = fields.IntEnumField(enum_type = PlanEnum, null = True)
    
    account_setting: fields.OneToOneRelation[AccountSetting] = fields.OneToOneField(
        "models.AccountSetting",
        related_name="account"
    )

    def __repr__(self) -> str:
        return f'Account(contract_id: "{self.contract_id}", status: "{self.user_sutatus}", plan: "{self.plan}")'

    @property
    def contractId(self):
        return self.contract_id

    @contractId.setter
    def contractId(self, contractId):
        self.contract_id = contractId

    @property
    def accessToken(self):
        accessToken = AccessToken(self.access_token, self.expiration_date_time)
        return accessToken

    @accessToken.setter
    def accessToken(self, accessToken):
        self.access_token = accessToken.accessToken
        self.expiration_date_time = accessToken.expirationDatetime

    @property
    def expirationDatetime(self):
        return self.expiration_date_time

    @property
    def userStatus(self):
        return self.user_status

    @userStatus.setter
    def userStatus(self, value):
        self.user_status = value

    @property
    async def accountSetting(self) -> AccountSetting:
        print (type(self.account_setting))
        if type(self.account_setting) == AccountSetting:
            return self.account_setting 
        return await self.account_setting.all()

    @classmethod
    async def create(cls, contractId, accessToken, plan=None):
        newAccountSetting = await AccountSetting.create(
            contract_id = contractId
        )

        newAccount = await super().create(
            contract_id = contractId,
            access_token = accessToken.accessToken,
            expiration_date_time = accessToken.expirationDatetime,
            user_status = cls.StatusEnum.STATUS_START,
            plan = plan,
            account_setting = newAccountSetting
        )
        return newAccount

