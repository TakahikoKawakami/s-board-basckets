from pydantic import BaseModel
import datetime


class NotificationId(BaseModel):
    __root__: int


class Notification(BaseModel):
    """お知らせentity
    """
    notification_id: NotificationId
    summary: str
    detail: str
    timestamp: datetime.date
