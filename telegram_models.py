from typing import List, Dict, Generic, TypeVar
from pydantic import BaseModel, Field, NoneStr
from pydantic.generics import GenericModel
from datetime import datetime
from enum import Enum

NoneInt = int | None


class ChatType(str, Enum):
    saved_messages = 'saved_messages'
    personal_chat = 'personal_chat'


class ContactCategory(str, Enum):
    people = 'people'
    bots = 'inline_bots'
    calls = 'calls'


class MessageType(str, Enum):
    message = 'message'
    service = 'service'


class MediaType(str, Enum):
    animation = "animation"
    video_file = "video_file"
    video_message = "video_message"
    voice_message = "voice_message"
    audio_file = "audio_file"
    sticker = "sticker"


class Message(BaseModel):
    date: datetime
    id_: int = Field(..., alias='id')
    text_entities: List[Dict]
    type: MessageType
    text: str | List[Dict | str]
    # other fields is optional

    # fields with > 1% count:
    from_: NoneStr = Field(None, alias='from')
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

    def getPlainText(self):
        if not self.text:
            return ''
        if isinstance(self.text, str):
            return self.text
        return ''.join(e['text'] for e in self.text_entities)
        # примечание: если в сообщении есть ссылка, будет сохранено только ее название, а не сама ссылка (href)


class Contact(BaseModel):
    date: str
    date_unixtime: int
    first_name: str
    last_name: str
    phone_number: str


class FrequentContact(BaseModel):
    id_: int = Field(..., alias='id')
    name: str
    rating: float
    category: ContactCategory


TData = TypeVar('TData')


class AboutWrapper(GenericModel, Generic[TData]):
    about: str
    list: List[TData]


# две главные модели

class TelegramChat(BaseModel):
    id_: int = Field(..., alias='id')
    messages: List[Message]
    name: NoneStr
    type_: ChatType = Field(..., alias='type')


class TelegramExport(BaseModel):
    chats: AboutWrapper[TelegramChat]
    contacts: AboutWrapper[Contact]
    frequent_contacts: AboutWrapper[FrequentContact]
