from functools import partial
from telegram_models import *
from pydantic import BaseModel, Field, NoneStr, validator
from typing import List, Dict, Tuple
from datetime import timedelta
from math import cos, pi

NoneFloat = float | None


class ContextData(Message):
    # TODO: use this in next version for storing voice messages, photos, etc.
    pass


class Chunk(BaseModel):
    context: List[Message]
    reply: Message

    # delta не обязательное поле
    delta: timedelta | None

    relevance: NoneFloat = Field(None, ge=0, le=1)
    specificity: NoneFloat = Field(None, ge=0, le=1)
    toxicity: NoneFloat = Field(None, ge=0, le=1)

    @validator('delta', pre=True, always=True)
    def calc_delta(cls, v, values):
        return values['reply'].date - values['context'][-1].date

    def to_text(self):  # ? for debug
        texts = [(message, message.text)
                 for message in self.context] + [(self.reply, self.reply.text)]
        texts = [(message, (text if text else '<empty>'))
                 for message, text in texts]
        # add date to each message
        texts = [
            f'{message.date.strftime("%d.%m.%Y %H:%M:%S")} - {text}' for message, text in texts]
        return '\n'.join(texts)


# splitting all messages into chunks

def get_chunk(messages: List[Message], reply_pos: int, max_context: int) -> Chunk:
    *context, reply = messages[max(reply_pos - max_context, 0): reply_pos + 1]
    return Chunk(context=context, reply=reply)


def split_messages(messages: List[Message], max_context: int = 3, min_context: int = 1) -> List[Chunk]:
    # TODO: rename to get_chunks
    return [get_chunk(messages, i, max_context) for i in range(min_context, len(messages))]


# splitting all chunks into dialog logical parts

class SplitSettings(BaseModel):
    delta_start: timedelta = timedelta(minutes=5)
    delta_end: timedelta = timedelta(hours=9)

    # параметры модели релевантности
    max_weight: float = 0.95
    min_weight: float = 0.05
    max_context: int = 3
    min_context: int = 1


def relevance_model_weight(time_delta, settings: SplitSettings = SplitSettings()):
    # если значения меньше минимального, то решение модели имеет минимальное значение
    if time_delta < settings.delta_start:
        return settings.min_weight
    elif time_delta > settings.delta_end:
        return settings.max_weight  # решение модели имеет максимальное значение
    else:
        d = settings.max_weight - settings.min_weight
        v = cos(pi * (time_delta - settings.delta_start) /
                (settings.delta_end - settings.delta_start))
        v = d * (1 - v) / 2 + settings.min_weight
        return v  # решение модели имеет значение между минимальным и максимальным


def precompute_relevance():
    pass


def get_relevance_specificity(chunk: Chunk):
    return 0.5, 0.5

# TODO: optimize for GPU

# TODO: somehow use specificity


def decide_relevance(chunk: Chunk, settings: SplitSettings = SplitSettings()):
    model_weight = relevance_model_weight(chunk.delta, settings)
    if model_weight == 0:
        # если дельта настолько мала, что решение модели не требуется,
        # то считаем, сообщение релевантно
        return True

    # в противном случае вычисляем релевантность с помощью модели
    # и решаем, релевантно ли сообщение с учетом решения модели
    relevance, _ = get_relevance_specificity(chunk)
    threshold = model_weight / 2

    if relevance >= (1 - threshold):
        return True
    if relevance <= threshold:
        return False

    return model_weight >= 0.5


def split_chunks(chunks: List[Chunk], settings: SplitSettings = SplitSettings()) -> List[Chunk]:
    parts = []
    current_part = [chunks[0]]
    for i in range(1, len(chunks)):
        prev_chunk, chunk = chunks[i - 1], chunks[i]
        # TODO: prev_chunk will be used later
        if decide_relevance(chunk, settings):
            current_part.append(chunk)
        else:
            parts.append(current_part)
            current_part = [chunk]

    if current_part:
        parts.append(current_part)

    return parts


# TODO: split_chunks в три этапа:
# 1. предобработка
# 2. вычисление средних значений релевантности
# 3. разделение на части

# для тестов можно не использовать модель при сплите сообщений с минимальной дельтой
split_chunks_test = partial(split_chunks, settings=SplitSettings(min_weight=0))
