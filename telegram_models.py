# Pydantic models for parsing Telegram Export files
# Author: Denis Churilov (Cyber Potato @ GitHub)
# Note: Some fields are omitted for simplicity and space saving


from pydantic import BaseModel, Field, NoneStr, validator
from typing import List, Dict
from datetime import datetime
from enum import Enum

NoneInt = int | None


class ChatType(str, Enum):
    Saved = 'saved_messages'
    Chat = 'personal_chat'


class ContactCategory(str, Enum):
    People = 'people'
    Bots = 'inline_bots'
    Call = 'calls'


class MessageType(str, Enum):
    Message = 'message'
    Service = 'service'


class MediaType(str, Enum):
    Animation = 'animation'
    Video = 'video_file'
    VideoMessage = 'video_message'
    VoiceMessage = 'voice_message'
    AudioFile = 'audio_file'
    Sticker = 'sticker'


class Message(BaseModel):
    date: datetime
    id_: int = Field(..., alias='id')
    text_entities: List[Dict]
    type: MessageType
    text: str
    # другие поля опциональны

    # поля, у которых процент встречаемости больше 1%
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

    # преобразуем список текстовых объектов в строку
    @validator('text', pre=True)
    def plain_text(cls, value) -> str:
        if isinstance(value, List):
            return ''.join(e.get('text', '') if isinstance(e, dict) else e for e in value)
        return value


class Contact(BaseModel):
    date: datetime
    first_name: str
    last_name: str
    phone_number: str


class FrequentContact(BaseModel):
    id_: int = Field(..., alias='id')
    name: str
    rating: float
    category: ContactCategory


# Две главные модели:
# TelegramExport - все данные из экспорта
# TelegramChat - данные об одном чате


class TelegramChat(BaseModel):
    id_: int = Field(..., alias='id')
    messages: List[Message]
    name: NoneStr
    type_: ChatType = Field(..., alias='type')

    def get_message(self, message_id: int) -> Message | None:
        return next((message for message in self.messages if message.id_ == message_id), None)


class TelegramExport(BaseModel):
    chats: List[TelegramChat]
    contacts: List[Contact]
    frequent_contacts: List[FrequentContact]

    # убираем обертку, если она есть
    @validator('chats', 'contacts', 'frequent_contacts', pre=True)
    def unwrap(cls, value) -> list:
        if isinstance(value, dict) and 'about' in value and 'list' in value:
            return value['list']
        return value
