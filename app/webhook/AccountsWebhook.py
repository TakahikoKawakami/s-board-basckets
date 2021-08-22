from app.common.abstracts.AbstractWebhook import AbstractWebhook
from app.domains.AccountDomainService import AccountDomainService
from app.domains.BasketDomainService import BasketDomainService

# from app.domains.TransactionsRepository import TransactionsRepository
# from app.domains.BasketAnalysesRepository import BasketAnalysesRepository

class AccountsWebhook(AbstractWebhook):
    ACTION_START = 'start'
    ACTION_END = 'end'
    ACTION_CHANGE_PLAN = 'change-plan'

    def __init__(self, loginAccount):
        super().__init__(loginAccount)
        
    async def received(self, event, body):
        self._logger.info('app subscription webhook received')

        action = body.get('action')
        planName = body.get('plan').get('name')
        
        if action == self.ACTION_START:
            await self.start(planName)
            return
        if action == self.ACTION_END:
            await self.end()
            return
        if action == self.ACTION_CHANGE_PLAN:
            await self.changePran(planName)
            return


    async def start(self, planName: str):
        """ユーザを新規登録します

        Args:
            planName (str): [description]
        """
        self._logger.info("新規登録")
        accountDomainService = await AccountDomainService.createInstance(self._accessAccount)
        await accountDomainService.signUpAccount(self._accessAccount.contractId, planName)


    async def changePlan(self, planName: str):
        """プランを変更します

        Args:
            planName (str): [description]
        """
        self._logger.info("プラン変更")
        accountDomainService = await AccountDomainService.createInstance(self._accessAccount)
        await accountDomainService.changePlan(self._accessAccount.contractId, planName)
        pass


    async def end(self):
        """利用停止します
        """
        self._logger.info("利用停止")
        accountDomainService = await AccountDomainService.createInstance(self._accessAccount)
        await accountDomainService.breakOffAccount(self._accessAccount.contractId)