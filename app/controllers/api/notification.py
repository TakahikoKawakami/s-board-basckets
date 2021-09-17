from typing import cast
from app.common.abstracts.AbstractController import AbstractController
from app.repositories.notifications import NotificationRepository


class NotificationCollectionController(AbstractController):
    def __init__(self) -> None:
        super().__init__()
        self._basket_domain_service = None

    async def on_get(self, req, resp):
        if self.is_booking_redirect():
            return
        self._logger.info('get notification collection api start')

        all_notifications = NotificationRepository.get_all()
        result = [notification.json() for notification in all_notifications]
        # breakpoint()
        resp.media = result

        self._logger.info('get notification collection api end')
        return


class NotificationController(AbstractController):
    def __init__(self) -> None:
        super().__init__()
        self._basket_domain_service = None

    async def on_get(self, req, resp, *, notification_id):
        if self.is_booking_redirect():
            return
        self._logger.info('get notification api start')

        result = NotificationRepository.find(int(notification_id))
        self._logger.debug(result)

        resp.media = result.json()

        self._logger.info('get notification api end')
        return
