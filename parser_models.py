from telegram_models import *
from pydantic import BaseModel, Field, NoneStr, validator
from typing import List, Dict
from datetime import timedelta


NoneFloat = float | None


class ContextData(Message):
    pass


class Chunk(BaseModel):
    context: List[Message]
    reply: Message

    # delta не обязательное поле
    delta: timedelta | None = Field(None, ge=timedelta(0))

    relevance: NoneFloat = Field(None, ge=0, le=1)
    specifity: NoneFloat = Field(None, ge=0, le=1)
    toxicity: NoneFloat = Field(None, ge=0, le=1)

    @validator('delta', pre=True, always=True)
    def calc_delta(cls, v, values):
        return values['reply'].date - values['context'][-1].date


def get_chunk(messages: List[Message], reply_pos: int, max_context: int) -> Chunk:
    *context, reply = messages[max(reply_pos - max_context, 0): reply_pos + 1]
    return Chunk(context=context, reply=reply)


def split_messages(messages: List[Message], max_context: int = 3, min_context: int = 1) -> List[Chunk]:
    return [get_chunk(messages, i, max_context) for i in range(min_context, len(messages))]
