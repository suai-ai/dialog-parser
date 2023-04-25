from typing import List, Dict, Generic, TypeVar
from pydantic import BaseModel, Field, NoneStr, validator
from pydantic.generics import GenericModel
from datetime import datetime
from enum import Enum

NoneInt = int | None


class ChatType(str, Enum):
    saved_messages = "saved_messages"
    personal_chat = "personal_chat"


class ContactCategory(str, Enum):
    people = "people"
    bots = "inline_bots"
    calls = "calls"


class MessageType(str, Enum):
    message = "message"
    service = "service"


class MediaType(str, Enum):
    animation = "animation"
    video_file = "video_file"
    video_message = "video_message"
    voice_message = "voice_message"
    audio_file = "audio_file"
    sticker = "sticker"


class Message(BaseModel):
    date: datetime
    id_: int = Field(..., alias="id")
    text_entities: List[Dict]
    type: MessageType
    text: str
    # другие поля опциональны

    # поля, у которых процент встречаемости больше 1%
    from_: NoneStr = Field(None, alias="from")
    from_id: NoneStr
    reply_to_message_id: NoneInt
    edited: datetime | None
    file: NoneStr
    thumbnail: NoneStr
    media_type: MediaType | None
    mime_type: NoneStr
    photo: NoneStr
    width: NoneInt
    height: NoneInt
    duration_seconds: NoneInt
    forwarded_from: NoneStr
    sticker_emoji: NoneStr

    # преобразуем список текстовых объектов в строку
    @validator("text", pre=True)
    def plain_text(cls, value):
        if isinstance(value, List):
            return "".join(
                e.get("text", "") if isinstance(e, dict) else e for e in value
            )
        return value


class Contact(BaseModel):
    date: str
    date_unixtime: int
    first_name: str
    last_name: str
    phone_number: str


class FrequentContact(BaseModel):
    id_: int = Field(..., alias="id")
    name: str
    rating: float
    category: ContactCategory


# обертка для списка с описанием

TData = TypeVar("TData")


class AboutWrapper(GenericModel, Generic[TData]):
    about: str
    list: List[TData]


T = TypeVar("T")
ListWrapper = AboutWrapper[T] | List[T]


# две главные модели:
# TelegramExport - все данные из экспорта
# TelegramChat - данные об одном чате


class TelegramChat(BaseModel):
    id_: int = Field(..., alias="id")
    messages: List[Message]
    name: NoneStr
    type_: ChatType = Field(..., alias="type")


class TelegramExport(BaseModel):
    chats: ListWrapper[TelegramChat]
    contacts: ListWrapper[Contact]
    frequent_contacts: ListWrapper[FrequentContact]

    # убираем обертку, если она есть
    @validator("chats", "contacts", "frequent_contacts", pre=True)
    def unwrap(cls, value):
        if isinstance(value, dict) and "about" in value and "list" in value:
            return value["list"]
        return value
