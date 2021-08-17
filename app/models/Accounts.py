from enum import Enum, IntEnum, auto
from tortoise import fields

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
        abstract = False
        table = "account_setting"


class Account(AbstractTortoiseModel):
    """
    アカウントモデル
    """

    class Meta:
        abstract = False
        table = "accounts"

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
            elif enum == cls.STANDARD:
                return "スタンダードプラン"
            elif enum == cls.PREMIUM:
                return "プレミアムプラン"
            else:
                return "プレミアムプラン"

        @classmethod
        def getPlanEnumValue(cls, planName: str) -> int:
            """プラン名からenum値を返します

            Args:
                planName (str): [description]

            Returns:
                int: [description]
            """
            if planName == "フリープラン":
                return cls.FREE
            elif planName == "スタンダードプラン":
                return cls.STANDARD
            elif planName == "プレミアムプラン":
                return cls.PREMIUM
            else:
                return cls.PREMIUM

    class StatusEnum(IntEnum):
        STATUS_START = 0
        STATUS_STOP = auto()

    class LoginStatusEnum(Enum):
        SIGN_UP = 0
        SIGN_IN = auto()
        SIGN_ON = auto()
        SIGN_OUT = auto()

    login_status = LoginStatusEnum.SIGN_ON

    access_token = fields.CharField(max_length=1024)
    expiration_date_time = fields.DatetimeField()
    status = fields.CharField(max_length=16, null=True)
    user_status = fields.IntEnumField(enum_type=StatusEnum)
    plan = fields.IntEnumField(enum_type=PlanEnum, null=True)
    last_login_version = fields.CharField(max_length=32, null=True)

    account_setting: fields.OneToOneRelation[AccountSetting] = \
        fields.OneToOneField(
            "models.AccountSetting",
            related_name="account"
        )

    def __repr__(self) -> str:
        return f'''
            Account(
                contract_id: "{self.contract_id}",
                status: "{self.user_status}",
                plan: "{self.plan}"
            )
        '''

    @property
    def access_token_entity(self):
        access_token = AccessToken(
            self.access_token,
            self.expiration_date_time
        )
        return access_token

    @access_token_entity.setter
    def access_token_entity(self, access_token: AccessToken):
        self.access_token = access_token.token
        self.expiration_date_time = access_token.expiration_datetime

    @property
    def expiration_datetime(self):
        return self.expiration_date_time

    @property
    async def account_setting_model(self) -> "AccountSetting":
        if type(self.account_setting) == AccountSetting:
            return self.account_setting
        return await self.account_setting.all()

    @classmethod
    async def create(cls, contract_id, access_token, plan=None):
        new_account_setting = await AccountSetting.create(
            contract_id=contract_id
        )

        new_account = await super().create(
            contract_id=contract_id,
            access_token=access_token.token,
            expiration_date_time=access_token.expiration_datetime,
            user_status=cls.StatusEnum.STATUS_START,
            plan=plan,
            account_setting=new_account_setting
        )
        return new_account


login_account = Account()
