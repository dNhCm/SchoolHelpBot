from abc import ABC
from typing import Optional, TypeVar, Any

from aiogram.fsm.context import FSMContext
from aiogram.handlers import BaseHandler
from aiogram.types import Message, User, Chat

T = TypeVar('T')


class CustomMessageHandler(BaseHandler[Message], ABC):
    """
    Base class for message handlers
    """

    def __init__(self, event: T, state: FSMContext, **kwargs: Any):
        super().__init__(event, **kwargs)
        self._state = state

    @property
    def from_user(self) -> Optional[User]:
        return self.event.from_user

    @property
    def chat(self) -> Chat:
        return self.event.chat

    @property
    def state(self) -> FSMContext:
        return self._state
