from abc import ABC
from typing import Any, TypeVar, Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.handlers import BaseHandler
from aiogram.types import CallbackQuery, Message, User

T = TypeVar("T")


class CustomCallbackQueryHandler(BaseHandler[CallbackQuery], ABC):
    def __init__(self, event: T, callback_data: Optional[CallbackData], **kwargs: Any):
        super().__init__(event, **kwargs)
        self._callback_data = callback_data

    @property
    def from_user(self) -> User:
        """
        Is alias for `event.from_user`
        """
        return self.event.from_user

    @property
    def message(self) -> Optional[Message]:
        """
        Is alias for `event.message`
        """
        return self.event.message

    @property
    def callback_data(self) -> Optional[CallbackData]:
        """
        Is modern alias for `event.data`
        """
        return self._callback_data
