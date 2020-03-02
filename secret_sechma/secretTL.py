from telethon.tl.tlobject import TLObject
from typing import Optional, List, Union, TYPE_CHECKING
import os
import struct
from datetime import datetime

if TYPE_CHECKING:
    from telethon.tl.types import TypeDecryptedMessage, TypeDecryptedMessageAction, TypeDecryptedMessageMedia, \
        TypeDocumentAttribute, TypeFileLocation, TypeInputStickerSet, TypeMessageEntity, TypePhotoSize, \
        TypeSendMessageAction


class DecryptedMessage(TLObject):
    CONSTRUCTOR_ID = 0x91cc4674
    SUBCLASS_OF_ID = 0x5182c3e8

    def __init__(self, ttl: int, message: str, random_id: int = None,
                 media: Optional['TypeDecryptedMessageMedia'] = None,
                 entities: Optional[List['TypeMessageEntity']] = None, via_bot_name: Optional[str] = None,
                 reply_to_random_id: Optional[int] = None, grouped_id: Optional[int] = None):
        """
        Constructor for secret.DecryptedMessage: Instance of either DecryptedMessage8, DecryptedMessageService8, DecryptedMessage23, DecryptedMessageService, DecryptedMessage46, DecryptedMessage.
        """
        self.ttl = ttl
        self.message = message
        self.random_id = random_id if random_id is not None else int.from_bytes(os.urandom(8), 'big', signed=True)
        self.media = media
        self.entities = entities
        self.via_bot_name = via_bot_name
        self.reply_to_random_id = reply_to_random_id
        self.grouped_id = grouped_id

    def to_dict(self):
        return {
            '_': 'DecryptedMessage',
            'ttl': self.ttl,
            'message': self.message,
            'random_id': self.random_id,
            'media': self.media.to_dict() if isinstance(self.media, TLObject) else self.media,
            'entities': [] if self.entities is None else [x.to_dict() if isinstance(x, TLObject) else x for x in
                                                          self.entities],
            'via_bot_name': self.via_bot_name,
            'reply_to_random_id': self.reply_to_random_id,
            'grouped_id': self.grouped_id
        }

    def __bytes__(self):
        return b''.join((
            b'tF\xcc\x91',
            struct.pack('<I', (0 if self.media is None or self.media is False else 512) | (
                0 if self.entities is None or self.entities is False else 128) | (
                            0 if self.via_bot_name is None or self.via_bot_name is False else 2048) | (
                            0 if self.reply_to_random_id is None or self.reply_to_random_id is False else 8) | (
                            0 if self.grouped_id is None or self.grouped_id is False else 131072)),
            struct.pack('<q', self.random_id),
            struct.pack('<i', self.ttl),
            self.serialize_bytes(self.message),
            b'' if self.media is None or self.media is False else (bytes(self.media)),
            b'' if self.entities is None or self.entities is False else b''.join((b'\x15\xc4\xb5\x1c',
                                                                                  struct.pack('<i', len(self.entities)),
                                                                                  b''.join(bytes(x) for x in
                                                                                           self.entities))),
            b'' if self.via_bot_name is None or self.via_bot_name is False else (
                self.serialize_bytes(self.via_bot_name)),
            b'' if self.reply_to_random_id is None or self.reply_to_random_id is False else (
                struct.pack('<q', self.reply_to_random_id)),
            b'' if self.grouped_id is None or self.grouped_id is False else (struct.pack('<q', self.grouped_id)),
        ))

    @classmethod
    def from_reader(cls, reader):
        flags = reader.read_int()

        _random_id = reader.read_long()
        _ttl = reader.read_int()
        _message = reader.tgread_string()
        if flags & 512:
            _media = reader.tgread_object()
        else:
            _media = None
        if flags & 128:
            reader.read_int()
            _entities = []
            for _ in range(reader.read_int()):
                _x = reader.tgread_object()
                _entities.append(_x)

        else:
            _entities = None
        if flags & 2048:
            _via_bot_name = reader.tgread_string()
        else:
            _via_bot_name = None
        if flags & 8:
            _reply_to_random_id = reader.read_long()
        else:
            _reply_to_random_id = None
        if flags & 131072:
            _grouped_id = reader.read_long()
        else:
            _grouped_id = None
        return cls(ttl=_ttl, message=_message, random_id=_random_id, media=_media, entities=_entities,
                   via_bot_name=_via_bot_name, reply_to_random_id=_reply_to_random_id, grouped_id=_grouped_id)


class DecryptedMessage23(TLObject):
    CONSTRUCTOR_ID = 0x204d3878
    SUBCLASS_OF_ID = 0x5182c3e8

    def __init__(self, ttl: int, message: str, media: 'TypeDecryptedMessageMedia', random_id: int = None):
        """
        Constructor for secret.DecryptedMessage: Instance of either DecryptedMessage8, DecryptedMessageService8, DecryptedMessage23, DecryptedMessageService, DecryptedMessage46, DecryptedMessage.
        """
        self.ttl = ttl
        self.message = message
        self.media = media
        self.random_id = random_id if random_id is not None else int.from_bytes(os.urandom(8), 'big', signed=True)

    def to_dict(self):
        return {
            '_': 'DecryptedMessage23',
            'ttl': self.ttl,
            'message': self.message,
            'media': self.media.to_dict() if isinstance(self.media, TLObject) else self.media,
            'random_id': self.random_id
        }

    def __bytes__(self):
        return b''.join((
            b'x8M ',
            struct.pack('<q', self.random_id),
            struct.pack('<i', self.ttl),
            self.serialize_bytes(self.message),
            bytes(self.media),
        ))

    @classmethod
    def from_reader(cls, reader):
        _random_id = reader.read_long()
        _ttl = reader.read_int()
        _message = reader.tgread_string()
        _media = reader.tgread_object()
        return cls(ttl=_ttl, message=_message, media=_media, random_id=_random_id)


class DecryptedMessage46(TLObject):
    CONSTRUCTOR_ID = 0x36b091de
    SUBCLASS_OF_ID = 0x5182c3e8

    def __init__(self, ttl: int, message: str, random_id: int = None,
                 media: Optional['TypeDecryptedMessageMedia'] = None,
                 entities: Optional[List['TypeMessageEntity']] = None, via_bot_name: Optional[str] = None,
                 reply_to_random_id: Optional[int] = None):
        """
        Constructor for secret.DecryptedMessage: Instance of either DecryptedMessage8, DecryptedMessageService8, DecryptedMessage23, DecryptedMessageService, DecryptedMessage46, DecryptedMessage.
        """
        self.ttl = ttl
        self.message = message
        self.random_id = random_id if random_id is not None else int.from_bytes(os.urandom(8), 'big', signed=True)
        self.media = media
        self.entities = entities
        self.via_bot_name = via_bot_name
        self.reply_to_random_id = reply_to_random_id

    def to_dict(self):
        return {
            '_': 'DecryptedMessage46',
            'ttl': self.ttl,
            'message': self.message,
            'random_id': self.random_id,
            'media': self.media.to_dict() if isinstance(self.media, TLObject) else self.media,
            'entities': [] if self.entities is None else [x.to_dict() if isinstance(x, TLObject) else x for x in
                                                          self.entities],
            'via_bot_name': self.via_bot_name,
            'reply_to_random_id': self.reply_to_random_id
        }

    def __bytes__(self):
        return b''.join((
            b'\xde\x91\xb06',
            struct.pack('<I', (0 if self.media is None or self.media is False else 512) | (
                0 if self.entities is None or self.entities is False else 128) | (
                            0 if self.via_bot_name is None or self.via_bot_name is False else 2048) | (
                            0 if self.reply_to_random_id is None or self.reply_to_random_id is False else 8)),
            struct.pack('<q', self.random_id),
            struct.pack('<i', self.ttl),
            self.serialize_bytes(self.message),
            b'' if self.media is None or self.media is False else (bytes(self.media)),
            b'' if self.entities is None or self.entities is False else b''.join((b'\x15\xc4\xb5\x1c',
                                                                                  struct.pack('<i', len(self.entities)),
                                                                                  b''.join(bytes(x) for x in
                                                                                           self.entities))),
            b'' if self.via_bot_name is None or self.via_bot_name is False else (
                self.serialize_bytes(self.via_bot_name)),
            b'' if self.reply_to_random_id is None or self.reply_to_random_id is False else (
                struct.pack('<q', self.reply_to_random_id)),
        ))

    @classmethod
    def from_reader(cls, reader):
        flags = reader.read_int()

        _random_id = reader.read_long()
        _ttl = reader.read_int()
        _message = reader.tgread_string()
        if flags & 512:
            _media = reader.tgread_object()
        else:
            _media = None
        if flags & 128:
            reader.read_int()
            _entities = []
            for _ in range(reader.read_int()):
                _x = reader.tgread_object()
                _entities.append(_x)

        else:
            _entities = None
        if flags & 2048:
            _via_bot_name = reader.tgread_string()
        else:
            _via_bot_name = None
        if flags & 8:
            _reply_to_random_id = reader.read_long()
        else:
            _reply_to_random_id = None
        return cls(ttl=_ttl, message=_message, random_id=_random_id, media=_media, entities=_entities,
                   via_bot_name=_via_bot_name, reply_to_random_id=_reply_to_random_id)


class DecryptedMessage8(TLObject):
    CONSTRUCTOR_ID = 0x1f814f1f
    SUBCLASS_OF_ID = 0x5182c3e8

    def __init__(self, random_bytes: bytes, message: str, media: 'TypeDecryptedMessageMedia', random_id: int = None):
        """
        Constructor for secret.DecryptedMessage: Instance of either DecryptedMessage8, DecryptedMessageService8, DecryptedMessage23, DecryptedMessageService, DecryptedMessage46, DecryptedMessage.
        """
        self.random_bytes = random_bytes
        self.message = message
        self.media = media
        self.random_id = random_id if random_id is not None else int.from_bytes(os.urandom(8), 'big', signed=True)

    def to_dict(self):
        return {
            '_': 'DecryptedMessage8',
            'random_bytes': self.random_bytes,
            'message': self.message,
            'media': self.media.to_dict() if isinstance(self.media, TLObject) else self.media,
            'random_id': self.random_id
        }

    def __bytes__(self):
        return b''.join((
            b'\x1fO\x81\x1f',
            struct.pack('<q', self.random_id),
            self.serialize_bytes(self.random_bytes),
            self.serialize_bytes(self.message),
            bytes(self.media),
        ))

    @classmethod
    def from_reader(cls, reader):
        _random_id = reader.read_long()
        _random_bytes = reader.tgread_bytes()
        _message = reader.tgread_string()
        _media = reader.tgread_object()
        return cls(random_bytes=_random_bytes, message=_message, media=_media, random_id=_random_id)


class DecryptedMessageActionAbortKey(TLObject):
    CONSTRUCTOR_ID = 0xdd05ec6b
    SUBCLASS_OF_ID = 0x3eecb877

    def __init__(self, exchange_id: int):
        """
        Constructor for secret.DecryptedMessageAction: Instance of either DecryptedMessageActionSetMessageTTL, DecryptedMessageActionReadMessages, DecryptedMessageActionDeleteMessages, DecryptedMessageActionScreenshotMessages, DecryptedMessageActionFlushHistory, DecryptedMessageActionResend, DecryptedMessageActionNotifyLayer, DecryptedMessageActionTyping, DecryptedMessageActionRequestKey, DecryptedMessageActionAcceptKey, DecryptedMessageActionAbortKey, DecryptedMessageActionCommitKey, DecryptedMessageActionNoop.
        """
        self.exchange_id = exchange_id

    def to_dict(self):
        return {
            '_': 'DecryptedMessageActionAbortKey',
            'exchange_id': self.exchange_id
        }

    def __bytes__(self):
        return b''.join((
            b'k\xec\x05\xdd',
            struct.pack('<q', self.exchange_id),
        ))

    @classmethod
    def from_reader(cls, reader):
        _exchange_id = reader.read_long()
        return cls(exchange_id=_exchange_id)


class DecryptedMessageActionAcceptKey(TLObject):
    CONSTRUCTOR_ID = 0x6fe1735b
    SUBCLASS_OF_ID = 0x3eecb877

    def __init__(self, exchange_id: int, g_b: bytes, key_fingerprint: int):
        """
        Constructor for secret.DecryptedMessageAction: Instance of either DecryptedMessageActionSetMessageTTL, DecryptedMessageActionReadMessages, DecryptedMessageActionDeleteMessages, DecryptedMessageActionScreenshotMessages, DecryptedMessageActionFlushHistory, DecryptedMessageActionResend, DecryptedMessageActionNotifyLayer, DecryptedMessageActionTyping, DecryptedMessageActionRequestKey, DecryptedMessageActionAcceptKey, DecryptedMessageActionAbortKey, DecryptedMessageActionCommitKey, DecryptedMessageActionNoop.
        """
        self.exchange_id = exchange_id
        self.g_b = g_b
        self.key_fingerprint = key_fingerprint

    def to_dict(self):
        return {
            '_': 'DecryptedMessageActionAcceptKey',
            'exchange_id': self.exchange_id,
            'g_b': self.g_b,
            'key_fingerprint': self.key_fingerprint
        }

    def __bytes__(self):
        return b''.join((
            b'[s\xe1o',
            struct.pack('<q', self.exchange_id),
            self.serialize_bytes(self.g_b),
            struct.pack('<q', self.key_fingerprint),
        ))

    @classmethod
    def from_reader(cls, reader):
        _exchange_id = reader.read_long()
        _g_b = reader.tgread_bytes()
        _key_fingerprint = reader.read_long()
        return cls(exchange_id=_exchange_id, g_b=_g_b, key_fingerprint=_key_fingerprint)


class DecryptedMessageActionCommitKey(TLObject):
    CONSTRUCTOR_ID = 0xec2e0b9b
    SUBCLASS_OF_ID = 0x3eecb877

    def __init__(self, exchange_id: int, key_fingerprint: int):
        """
        Constructor for secret.DecryptedMessageAction: Instance of either DecryptedMessageActionSetMessageTTL, DecryptedMessageActionReadMessages, DecryptedMessageActionDeleteMessages, DecryptedMessageActionScreenshotMessages, DecryptedMessageActionFlushHistory, DecryptedMessageActionResend, DecryptedMessageActionNotifyLayer, DecryptedMessageActionTyping, DecryptedMessageActionRequestKey, DecryptedMessageActionAcceptKey, DecryptedMessageActionAbortKey, DecryptedMessageActionCommitKey, DecryptedMessageActionNoop.
        """
        self.exchange_id = exchange_id
        self.key_fingerprint = key_fingerprint

    def to_dict(self):
        return {
            '_': 'DecryptedMessageActionCommitKey',
            'exchange_id': self.exchange_id,
            'key_fingerprint': self.key_fingerprint
        }

    def __bytes__(self):
        return b''.join((
            b'\x9b\x0b.\xec',
            struct.pack('<q', self.exchange_id),
            struct.pack('<q', self.key_fingerprint),
        ))

    @classmethod
    def from_reader(cls, reader):
        _exchange_id = reader.read_long()
        _key_fingerprint = reader.read_long()
        return cls(exchange_id=_exchange_id, key_fingerprint=_key_fingerprint)


class DecryptedMessageActionDeleteMessages(TLObject):
    CONSTRUCTOR_ID = 0x65614304
    SUBCLASS_OF_ID = 0x3eecb877

    def __init__(self, random_ids: List[int]):
        """
        Constructor for secret.DecryptedMessageAction: Instance of either DecryptedMessageActionSetMessageTTL, DecryptedMessageActionReadMessages, DecryptedMessageActionDeleteMessages, DecryptedMessageActionScreenshotMessages, DecryptedMessageActionFlushHistory, DecryptedMessageActionResend, DecryptedMessageActionNotifyLayer, DecryptedMessageActionTyping, DecryptedMessageActionRequestKey, DecryptedMessageActionAcceptKey, DecryptedMessageActionAbortKey, DecryptedMessageActionCommitKey, DecryptedMessageActionNoop.
        """
        self.random_ids = random_ids

    def to_dict(self):
        return {
            '_': 'DecryptedMessageActionDeleteMessages',
            'random_ids': [] if self.random_ids is None else self.random_ids[:]
        }

    def __bytes__(self):
        return b''.join((
            b'\x04Cae',
            b'\x15\xc4\xb5\x1c', struct.pack('<i', len(self.random_ids)),
            b''.join(struct.pack('<q', x) for x in self.random_ids),
        ))

    @classmethod
    def from_reader(cls, reader):
        reader.read_int()
        _random_ids = []
        for _ in range(reader.read_int()):
            _x = reader.read_long()
            _random_ids.append(_x)

        return cls(random_ids=_random_ids)


class DecryptedMessageActionFlushHistory(TLObject):
    CONSTRUCTOR_ID = 0x6719e45c
    SUBCLASS_OF_ID = 0x3eecb877

    def to_dict(self):
        return {
            '_': 'DecryptedMessageActionFlushHistory'
        }

    def __bytes__(self):
        return b''.join((
            b'\\\xe4\x19g',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class DecryptedMessageActionNoop(TLObject):
    CONSTRUCTOR_ID = 0xa82fdd63
    SUBCLASS_OF_ID = 0x3eecb877

    def to_dict(self):
        return {
            '_': 'DecryptedMessageActionNoop'
        }

    def __bytes__(self):
        return b''.join((
            b'c\xdd/\xa8',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class DecryptedMessageActionNotifyLayer(TLObject):
    CONSTRUCTOR_ID = 0xf3048883
    SUBCLASS_OF_ID = 0x3eecb877

    def __init__(self, layer: int):
        """
        Constructor for secret.DecryptedMessageAction: Instance of either DecryptedMessageActionSetMessageTTL, DecryptedMessageActionReadMessages, DecryptedMessageActionDeleteMessages, DecryptedMessageActionScreenshotMessages, DecryptedMessageActionFlushHistory, DecryptedMessageActionResend, DecryptedMessageActionNotifyLayer, DecryptedMessageActionTyping, DecryptedMessageActionRequestKey, DecryptedMessageActionAcceptKey, DecryptedMessageActionAbortKey, DecryptedMessageActionCommitKey, DecryptedMessageActionNoop.
        """
        self.layer = layer

    def to_dict(self):
        return {
            '_': 'DecryptedMessageActionNotifyLayer',
            'layer': self.layer
        }

    def __bytes__(self):
        return b''.join((
            b'\x83\x88\x04\xf3',
            struct.pack('<i', self.layer),
        ))

    @classmethod
    def from_reader(cls, reader):
        _layer = reader.read_int()
        return cls(layer=_layer)


class DecryptedMessageActionReadMessages(TLObject):
    CONSTRUCTOR_ID = 0xc4f40be
    SUBCLASS_OF_ID = 0x3eecb877

    def __init__(self, random_ids: List[int]):
        """
        Constructor for secret.DecryptedMessageAction: Instance of either DecryptedMessageActionSetMessageTTL, DecryptedMessageActionReadMessages, DecryptedMessageActionDeleteMessages, DecryptedMessageActionScreenshotMessages, DecryptedMessageActionFlushHistory, DecryptedMessageActionResend, DecryptedMessageActionNotifyLayer, DecryptedMessageActionTyping, DecryptedMessageActionRequestKey, DecryptedMessageActionAcceptKey, DecryptedMessageActionAbortKey, DecryptedMessageActionCommitKey, DecryptedMessageActionNoop.
        """
        self.random_ids = random_ids

    def to_dict(self):
        return {
            '_': 'DecryptedMessageActionReadMessages',
            'random_ids': [] if self.random_ids is None else self.random_ids[:]
        }

    def __bytes__(self):
        return b''.join((
            b'\xbe@O\x0c',
            b'\x15\xc4\xb5\x1c', struct.pack('<i', len(self.random_ids)),
            b''.join(struct.pack('<q', x) for x in self.random_ids),
        ))

    @classmethod
    def from_reader(cls, reader):
        reader.read_int()
        _random_ids = []
        for _ in range(reader.read_int()):
            _x = reader.read_long()
            _random_ids.append(_x)

        return cls(random_ids=_random_ids)


class DecryptedMessageActionRequestKey(TLObject):
    CONSTRUCTOR_ID = 0xf3c9611b
    SUBCLASS_OF_ID = 0x3eecb877

    def __init__(self, exchange_id: int, g_a: bytes):
        """
        Constructor for secret.DecryptedMessageAction: Instance of either DecryptedMessageActionSetMessageTTL, DecryptedMessageActionReadMessages, DecryptedMessageActionDeleteMessages, DecryptedMessageActionScreenshotMessages, DecryptedMessageActionFlushHistory, DecryptedMessageActionResend, DecryptedMessageActionNotifyLayer, DecryptedMessageActionTyping, DecryptedMessageActionRequestKey, DecryptedMessageActionAcceptKey, DecryptedMessageActionAbortKey, DecryptedMessageActionCommitKey, DecryptedMessageActionNoop.
        """
        self.exchange_id = exchange_id
        self.g_a = g_a

    def to_dict(self):
        return {
            '_': 'DecryptedMessageActionRequestKey',
            'exchange_id': self.exchange_id,
            'g_a': self.g_a
        }

    def __bytes__(self):
        return b''.join((
            b'\x1ba\xc9\xf3',
            struct.pack('<q', self.exchange_id),
            self.serialize_bytes(self.g_a),
        ))

    @classmethod
    def from_reader(cls, reader):
        _exchange_id = reader.read_long()
        _g_a = reader.tgread_bytes()
        return cls(exchange_id=_exchange_id, g_a=_g_a)


class DecryptedMessageActionResend(TLObject):
    CONSTRUCTOR_ID = 0x511110b0
    SUBCLASS_OF_ID = 0x3eecb877

    def __init__(self, start_seq_no: int, end_seq_no: int):
        """
        Constructor for secret.DecryptedMessageAction: Instance of either DecryptedMessageActionSetMessageTTL, DecryptedMessageActionReadMessages, DecryptedMessageActionDeleteMessages, DecryptedMessageActionScreenshotMessages, DecryptedMessageActionFlushHistory, DecryptedMessageActionResend, DecryptedMessageActionNotifyLayer, DecryptedMessageActionTyping, DecryptedMessageActionRequestKey, DecryptedMessageActionAcceptKey, DecryptedMessageActionAbortKey, DecryptedMessageActionCommitKey, DecryptedMessageActionNoop.
        """
        self.start_seq_no = start_seq_no
        self.end_seq_no = end_seq_no

    def to_dict(self):
        return {
            '_': 'DecryptedMessageActionResend',
            'start_seq_no': self.start_seq_no,
            'end_seq_no': self.end_seq_no
        }

    def __bytes__(self):
        return b''.join((
            b'\xb0\x10\x11Q',
            struct.pack('<i', self.start_seq_no),
            struct.pack('<i', self.end_seq_no),
        ))

    @classmethod
    def from_reader(cls, reader):
        _start_seq_no = reader.read_int()
        _end_seq_no = reader.read_int()
        return cls(start_seq_no=_start_seq_no, end_seq_no=_end_seq_no)


class DecryptedMessageActionScreenshotMessages(TLObject):
    CONSTRUCTOR_ID = 0x8ac1f475
    SUBCLASS_OF_ID = 0x3eecb877

    def __init__(self, random_ids: List[int]):
        """
        Constructor for secret.DecryptedMessageAction: Instance of either DecryptedMessageActionSetMessageTTL, DecryptedMessageActionReadMessages, DecryptedMessageActionDeleteMessages, DecryptedMessageActionScreenshotMessages, DecryptedMessageActionFlushHistory, DecryptedMessageActionResend, DecryptedMessageActionNotifyLayer, DecryptedMessageActionTyping, DecryptedMessageActionRequestKey, DecryptedMessageActionAcceptKey, DecryptedMessageActionAbortKey, DecryptedMessageActionCommitKey, DecryptedMessageActionNoop.
        """
        self.random_ids = random_ids

    def to_dict(self):
        return {
            '_': 'DecryptedMessageActionScreenshotMessages',
            'random_ids': [] if self.random_ids is None else self.random_ids[:]
        }

    def __bytes__(self):
        return b''.join((
            b'u\xf4\xc1\x8a',
            b'\x15\xc4\xb5\x1c', struct.pack('<i', len(self.random_ids)),
            b''.join(struct.pack('<q', x) for x in self.random_ids),
        ))

    @classmethod
    def from_reader(cls, reader):
        reader.read_int()
        _random_ids = []
        for _ in range(reader.read_int()):
            _x = reader.read_long()
            _random_ids.append(_x)

        return cls(random_ids=_random_ids)


class DecryptedMessageActionSetMessageTTL(TLObject):
    CONSTRUCTOR_ID = 0xa1733aec
    SUBCLASS_OF_ID = 0x3eecb877

    def __init__(self, ttl_seconds: int):
        """
        Constructor for secret.DecryptedMessageAction: Instance of either DecryptedMessageActionSetMessageTTL, DecryptedMessageActionReadMessages, DecryptedMessageActionDeleteMessages, DecryptedMessageActionScreenshotMessages, DecryptedMessageActionFlushHistory, DecryptedMessageActionResend, DecryptedMessageActionNotifyLayer, DecryptedMessageActionTyping, DecryptedMessageActionRequestKey, DecryptedMessageActionAcceptKey, DecryptedMessageActionAbortKey, DecryptedMessageActionCommitKey, DecryptedMessageActionNoop.
        """
        self.ttl_seconds = ttl_seconds

    def to_dict(self):
        return {
            '_': 'DecryptedMessageActionSetMessageTTL',
            'ttl_seconds': self.ttl_seconds
        }

    def __bytes__(self):
        return b''.join((
            b'\xec:s\xa1',
            struct.pack('<i', self.ttl_seconds),
        ))

    @classmethod
    def from_reader(cls, reader):
        _ttl_seconds = reader.read_int()
        return cls(ttl_seconds=_ttl_seconds)


class DecryptedMessageActionTyping(TLObject):
    CONSTRUCTOR_ID = 0xccb27641
    SUBCLASS_OF_ID = 0x3eecb877

    def __init__(self, action: 'TypeSendMessageAction'):
        """
        Constructor for secret.DecryptedMessageAction: Instance of either DecryptedMessageActionSetMessageTTL, DecryptedMessageActionReadMessages, DecryptedMessageActionDeleteMessages, DecryptedMessageActionScreenshotMessages, DecryptedMessageActionFlushHistory, DecryptedMessageActionResend, DecryptedMessageActionNotifyLayer, DecryptedMessageActionTyping, DecryptedMessageActionRequestKey, DecryptedMessageActionAcceptKey, DecryptedMessageActionAbortKey, DecryptedMessageActionCommitKey, DecryptedMessageActionNoop.
        """
        self.action = action

    def to_dict(self):
        return {
            '_': 'DecryptedMessageActionTyping',
            'action': self.action.to_dict() if isinstance(self.action, TLObject) else self.action
        }

    def __bytes__(self):
        return b''.join((
            b'Av\xb2\xcc',
            bytes(self.action),
        ))

    @classmethod
    def from_reader(cls, reader):
        _action = reader.tgread_object()
        return cls(action=_action)


class DecryptedMessageLayer(TLObject):
    CONSTRUCTOR_ID = 0x1be31789
    SUBCLASS_OF_ID = 0x18576013

    def __init__(self, random_bytes: bytes, layer: int, in_seq_no: int, out_seq_no: int,
                 message: 'TypeDecryptedMessage'):
        """
        Constructor for secret.DecryptedMessageLayer: Instance of DecryptedMessageLayer.
        """
        self.random_bytes = random_bytes
        self.layer = layer
        self.in_seq_no = in_seq_no
        self.out_seq_no = out_seq_no
        self.message = message

    def to_dict(self):
        return {
            '_': 'DecryptedMessageLayer',
            'random_bytes': self.random_bytes,
            'layer': self.layer,
            'in_seq_no': self.in_seq_no,
            'out_seq_no': self.out_seq_no,
            'message': self.message.to_dict() if isinstance(self.message, TLObject) else self.message
        }

    def __bytes__(self):
        return b''.join((
            b'\x89\x17\xe3\x1b',
            self.serialize_bytes(self.random_bytes),
            struct.pack('<i', self.layer),
            struct.pack('<i', self.in_seq_no),
            struct.pack('<i', self.out_seq_no),
            bytes(self.message),
        ))

    @classmethod
    def from_reader(cls, reader):
        _random_bytes = reader.tgread_bytes()
        _layer = reader.read_int()
        _in_seq_no = reader.read_int()
        _out_seq_no = reader.read_int()
        _message = reader.tgread_object()
        return cls(random_bytes=_random_bytes, layer=_layer, in_seq_no=_in_seq_no, out_seq_no=_out_seq_no,
                   message=_message)


class DecryptedMessageMediaAudio(TLObject):
    CONSTRUCTOR_ID = 0x57e0a9cb
    SUBCLASS_OF_ID = 0x96a0e005

    def __init__(self, duration: int, mime_type: str, size: int, key: bytes, iv: bytes):
        """
        Constructor for secret.DecryptedMessageMedia: Instance of either DecryptedMessageMediaEmpty, DecryptedMessageMediaPhoto23, DecryptedMessageMediaVideo8, DecryptedMessageMediaGeoPoint, DecryptedMessageMediaContact, DecryptedMessageMediaDocument23, DecryptedMessageMediaAudio8, DecryptedMessageMediaVideo23, DecryptedMessageMediaAudio, DecryptedMessageMediaExternalDocument, DecryptedMessageMediaPhoto, DecryptedMessageMediaVideo, DecryptedMessageMediaDocument, DecryptedMessageMediaVenue, DecryptedMessageMediaWebPage.
        """
        self.duration = duration
        self.mime_type = mime_type
        self.size = size
        self.key = key
        self.iv = iv

    def to_dict(self):
        return {
            '_': 'DecryptedMessageMediaAudio',
            'duration': self.duration,
            'mime_type': self.mime_type,
            'size': self.size,
            'key': self.key,
            'iv': self.iv
        }

    def __bytes__(self):
        return b''.join((
            b'\xcb\xa9\xe0W',
            struct.pack('<i', self.duration),
            self.serialize_bytes(self.mime_type),
            struct.pack('<i', self.size),
            self.serialize_bytes(self.key),
            self.serialize_bytes(self.iv),
        ))

    @classmethod
    def from_reader(cls, reader):
        _duration = reader.read_int()
        _mime_type = reader.tgread_string()
        _size = reader.read_int()
        _key = reader.tgread_bytes()
        _iv = reader.tgread_bytes()
        return cls(duration=_duration, mime_type=_mime_type, size=_size, key=_key, iv=_iv)


class DecryptedMessageMediaAudio8(TLObject):
    CONSTRUCTOR_ID = 0x6080758f
    SUBCLASS_OF_ID = 0x96a0e005

    def __init__(self, duration: int, size: int, key: bytes, iv: bytes):
        """
        Constructor for secret.DecryptedMessageMedia: Instance of either DecryptedMessageMediaEmpty, DecryptedMessageMediaPhoto23, DecryptedMessageMediaVideo8, DecryptedMessageMediaGeoPoint, DecryptedMessageMediaContact, DecryptedMessageMediaDocument23, DecryptedMessageMediaAudio8, DecryptedMessageMediaVideo23, DecryptedMessageMediaAudio, DecryptedMessageMediaExternalDocument, DecryptedMessageMediaPhoto, DecryptedMessageMediaVideo, DecryptedMessageMediaDocument, DecryptedMessageMediaVenue, DecryptedMessageMediaWebPage.
        """
        self.duration = duration
        self.size = size
        self.key = key
        self.iv = iv

    def to_dict(self):
        return {
            '_': 'DecryptedMessageMediaAudio8',
            'duration': self.duration,
            'size': self.size,
            'key': self.key,
            'iv': self.iv
        }

    def __bytes__(self):
        return b''.join((
            b'\x8fu\x80`',
            struct.pack('<i', self.duration),
            struct.pack('<i', self.size),
            self.serialize_bytes(self.key),
            self.serialize_bytes(self.iv),
        ))

    @classmethod
    def from_reader(cls, reader):
        _duration = reader.read_int()
        _size = reader.read_int()
        _key = reader.tgread_bytes()
        _iv = reader.tgread_bytes()
        return cls(duration=_duration, size=_size, key=_key, iv=_iv)


class DecryptedMessageMediaContact(TLObject):
    CONSTRUCTOR_ID = 0x588a0a97
    SUBCLASS_OF_ID = 0x96a0e005

    def __init__(self, phone_number: str, first_name: str, last_name: str, user_id: int):
        """
        Constructor for secret.DecryptedMessageMedia: Instance of either DecryptedMessageMediaEmpty, DecryptedMessageMediaPhoto23, DecryptedMessageMediaVideo8, DecryptedMessageMediaGeoPoint, DecryptedMessageMediaContact, DecryptedMessageMediaDocument23, DecryptedMessageMediaAudio8, DecryptedMessageMediaVideo23, DecryptedMessageMediaAudio, DecryptedMessageMediaExternalDocument, DecryptedMessageMediaPhoto, DecryptedMessageMediaVideo, DecryptedMessageMediaDocument, DecryptedMessageMediaVenue, DecryptedMessageMediaWebPage.
        """
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id

    def to_dict(self):
        return {
            '_': 'DecryptedMessageMediaContact',
            'phone_number': self.phone_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'user_id': self.user_id
        }

    def __bytes__(self):
        return b''.join((
            b'\x97\n\x8aX',
            self.serialize_bytes(self.phone_number),
            self.serialize_bytes(self.first_name),
            self.serialize_bytes(self.last_name),
            struct.pack('<i', self.user_id),
        ))

    @classmethod
    def from_reader(cls, reader):
        _phone_number = reader.tgread_string()
        _first_name = reader.tgread_string()
        _last_name = reader.tgread_string()
        _user_id = reader.read_int()
        return cls(phone_number=_phone_number, first_name=_first_name, last_name=_last_name, user_id=_user_id)


class DecryptedMessageMediaDocument(TLObject):
    CONSTRUCTOR_ID = 0x7afe8ae2
    SUBCLASS_OF_ID = 0x96a0e005

    def __init__(self, thumb: bytes, thumb_w: int, thumb_h: int, mime_type: str, size: int, key: bytes, iv: bytes,
                 attributes: List['TypeDocumentAttribute'], caption: str):
        """
        Constructor for secret.DecryptedMessageMedia: Instance of either DecryptedMessageMediaEmpty, DecryptedMessageMediaPhoto23, DecryptedMessageMediaVideo8, DecryptedMessageMediaGeoPoint, DecryptedMessageMediaContact, DecryptedMessageMediaDocument23, DecryptedMessageMediaAudio8, DecryptedMessageMediaVideo23, DecryptedMessageMediaAudio, DecryptedMessageMediaExternalDocument, DecryptedMessageMediaPhoto, DecryptedMessageMediaVideo, DecryptedMessageMediaDocument, DecryptedMessageMediaVenue, DecryptedMessageMediaWebPage.
        """
        self.thumb = thumb
        self.thumb_w = thumb_w
        self.thumb_h = thumb_h
        self.mime_type = mime_type
        self.size = size
        self.key = key
        self.iv = iv
        self.attributes = attributes
        self.caption = caption

    def to_dict(self):
        return {
            '_': 'DecryptedMessageMediaDocument',
            'thumb': self.thumb,
            'thumb_w': self.thumb_w,
            'thumb_h': self.thumb_h,
            'mime_type': self.mime_type,
            'size': self.size,
            'key': self.key,
            'iv': self.iv,
            'attributes': [] if self.attributes is None else [x.to_dict() if isinstance(x, TLObject) else x for x in
                                                              self.attributes],
            'caption': self.caption
        }

    def __bytes__(self):
        return b''.join((
            b'\xe2\x8a\xfez',
            self.serialize_bytes(self.thumb),
            struct.pack('<i', self.thumb_w),
            struct.pack('<i', self.thumb_h),
            self.serialize_bytes(self.mime_type),
            struct.pack('<i', self.size),
            self.serialize_bytes(self.key),
            self.serialize_bytes(self.iv),
            b'\x15\xc4\xb5\x1c', struct.pack('<i', len(self.attributes)), b''.join(bytes(x) for x in self.attributes),
            self.serialize_bytes(self.caption),
        ))

    @classmethod
    def from_reader(cls, reader):
        _thumb = reader.tgread_bytes()
        _thumb_w = reader.read_int()
        _thumb_h = reader.read_int()
        _mime_type = reader.tgread_string()
        _size = reader.read_int()
        _key = reader.tgread_bytes()
        _iv = reader.tgread_bytes()
        reader.read_int()
        _attributes = []
        for _ in range(reader.read_int()):
            _x = reader.tgread_object()
            _attributes.append(_x)

        _caption = reader.tgread_string()
        return cls(thumb=_thumb, thumb_w=_thumb_w, thumb_h=_thumb_h, mime_type=_mime_type, size=_size, key=_key, iv=_iv,
                   attributes=_attributes, caption=_caption)


class DecryptedMessageMediaDocument23(TLObject):
    CONSTRUCTOR_ID = 0xb095434b
    SUBCLASS_OF_ID = 0x96a0e005

    def __init__(self, thumb: bytes, thumb_w: int, thumb_h: int, file_name: str, mime_type: str, size: int, key: bytes,
                 iv: bytes):
        """
        Constructor for secret.DecryptedMessageMedia: Instance of either DecryptedMessageMediaEmpty, DecryptedMessageMediaPhoto23, DecryptedMessageMediaVideo8, DecryptedMessageMediaGeoPoint, DecryptedMessageMediaContact, DecryptedMessageMediaDocument23, DecryptedMessageMediaAudio8, DecryptedMessageMediaVideo23, DecryptedMessageMediaAudio, DecryptedMessageMediaExternalDocument, DecryptedMessageMediaPhoto, DecryptedMessageMediaVideo, DecryptedMessageMediaDocument, DecryptedMessageMediaVenue, DecryptedMessageMediaWebPage.
        """
        self.thumb = thumb
        self.thumb_w = thumb_w
        self.thumb_h = thumb_h
        self.file_name = file_name
        self.mime_type = mime_type
        self.size = size
        self.key = key
        self.iv = iv

    def to_dict(self):
        return {
            '_': 'DecryptedMessageMediaDocument23',
            'thumb': self.thumb,
            'thumb_w': self.thumb_w,
            'thumb_h': self.thumb_h,
            'file_name': self.file_name,
            'mime_type': self.mime_type,
            'size': self.size,
            'key': self.key,
            'iv': self.iv
        }

    def __bytes__(self):
        return b''.join((
            b'KC\x95\xb0',
            self.serialize_bytes(self.thumb),
            struct.pack('<i', self.thumb_w),
            struct.pack('<i', self.thumb_h),
            self.serialize_bytes(self.file_name),
            self.serialize_bytes(self.mime_type),
            struct.pack('<i', self.size),
            self.serialize_bytes(self.key),
            self.serialize_bytes(self.iv),
        ))

    @classmethod
    def from_reader(cls, reader):
        _thumb = reader.tgread_bytes()
        _thumb_w = reader.read_int()
        _thumb_h = reader.read_int()
        _file_name = reader.tgread_string()
        _mime_type = reader.tgread_string()
        _size = reader.read_int()
        _key = reader.tgread_bytes()
        _iv = reader.tgread_bytes()
        return cls(thumb=_thumb, thumb_w=_thumb_w, thumb_h=_thumb_h, file_name=_file_name, mime_type=_mime_type,
                   size=_size, key=_key, iv=_iv)


class DecryptedMessageMediaEmpty(TLObject):
    CONSTRUCTOR_ID = 0x89f5c4a
    SUBCLASS_OF_ID = 0x96a0e005

    def to_dict(self):
        return {
            '_': 'DecryptedMessageMediaEmpty'
        }

    def __bytes__(self):
        return b''.join((
            b'J\\\x9f\x08',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class DecryptedMessageMediaExternalDocument(TLObject):
    CONSTRUCTOR_ID = 0xfa95b0dd
    SUBCLASS_OF_ID = 0x96a0e005

    # noinspection PyShadowingBuiltins
    def __init__(self, id: int, access_hash: int, date: Optional[datetime], mime_type: str, size: int,
                 thumb: 'TypePhotoSize', dc_id: int, attributes: List['TypeDocumentAttribute']):
        """
        Constructor for secret.DecryptedMessageMedia: Instance of either DecryptedMessageMediaEmpty, DecryptedMessageMediaPhoto23, DecryptedMessageMediaVideo8, DecryptedMessageMediaGeoPoint, DecryptedMessageMediaContact, DecryptedMessageMediaDocument23, DecryptedMessageMediaAudio8, DecryptedMessageMediaVideo23, DecryptedMessageMediaAudio, DecryptedMessageMediaExternalDocument, DecryptedMessageMediaPhoto, DecryptedMessageMediaVideo, DecryptedMessageMediaDocument, DecryptedMessageMediaVenue, DecryptedMessageMediaWebPage.
        """
        self.id = id
        self.access_hash = access_hash
        self.date = date
        self.mime_type = mime_type
        self.size = size
        self.thumb = thumb
        self.dc_id = dc_id
        self.attributes = attributes

    def to_dict(self):
        return {
            '_': 'DecryptedMessageMediaExternalDocument',
            'id': self.id,
            'access_hash': self.access_hash,
            'date': self.date,
            'mime_type': self.mime_type,
            'size': self.size,
            'thumb': self.thumb.to_dict() if isinstance(self.thumb, TLObject) else self.thumb,
            'dc_id': self.dc_id,
            'attributes': [] if self.attributes is None else [x.to_dict() if isinstance(x, TLObject) else x for x in
                                                              self.attributes]
        }

    def __bytes__(self):
        return b''.join((
            b'\xdd\xb0\x95\xfa',
            struct.pack('<q', self.id),
            struct.pack('<q', self.access_hash),
            self.serialize_datetime(self.date),
            self.serialize_bytes(self.mime_type),
            struct.pack('<i', self.size),
            bytes(self.thumb),
            struct.pack('<i', self.dc_id),
            b'\x15\xc4\xb5\x1c', struct.pack('<i', len(self.attributes)), b''.join(bytes(x) for x in self.attributes),
        ))

    @classmethod
    def from_reader(cls, reader):
        _id = reader.read_long()
        _access_hash = reader.read_long()
        _date = reader.tgread_date()
        _mime_type = reader.tgread_string()
        _size = reader.read_int()
        _thumb = reader.tgread_object()
        _dc_id = reader.read_int()
        reader.read_int()
        _attributes = []
        for _ in range(reader.read_int()):
            _x = reader.tgread_object()
            _attributes.append(_x)

        return cls(id=_id, access_hash=_access_hash, date=_date, mime_type=_mime_type, size=_size, thumb=_thumb,
                   dc_id=_dc_id, attributes=_attributes)


class DecryptedMessageMediaGeoPoint(TLObject):
    CONSTRUCTOR_ID = 0x35480a59
    SUBCLASS_OF_ID = 0x96a0e005

    def __init__(self, lat: float, long: float):
        """
        Constructor for secret.DecryptedMessageMedia: Instance of either DecryptedMessageMediaEmpty, DecryptedMessageMediaPhoto23, DecryptedMessageMediaVideo8, DecryptedMessageMediaGeoPoint, DecryptedMessageMediaContact, DecryptedMessageMediaDocument23, DecryptedMessageMediaAudio8, DecryptedMessageMediaVideo23, DecryptedMessageMediaAudio, DecryptedMessageMediaExternalDocument, DecryptedMessageMediaPhoto, DecryptedMessageMediaVideo, DecryptedMessageMediaDocument, DecryptedMessageMediaVenue, DecryptedMessageMediaWebPage.
        """
        self.lat = lat
        self.long = long

    def to_dict(self):
        return {
            '_': 'DecryptedMessageMediaGeoPoint',
            'lat': self.lat,
            'long': self.long
        }

    def __bytes__(self):
        return b''.join((
            b'Y\nH5',
            struct.pack('<d', self.lat),
            struct.pack('<d', self.long),
        ))

    @classmethod
    def from_reader(cls, reader):
        _lat = reader.read_double()
        _long = reader.read_double()
        return cls(lat=_lat, long=_long)


class DecryptedMessageMediaPhoto(TLObject):
    CONSTRUCTOR_ID = 0xf1fa8d78
    SUBCLASS_OF_ID = 0x96a0e005

    def __init__(self, thumb: bytes, thumb_w: int, thumb_h: int, w: int, h: int, size: int, key: bytes, iv: bytes,
                 caption: str):
        """
        Constructor for secret.DecryptedMessageMedia: Instance of either DecryptedMessageMediaEmpty, DecryptedMessageMediaPhoto23, DecryptedMessageMediaVideo8, DecryptedMessageMediaGeoPoint, DecryptedMessageMediaContact, DecryptedMessageMediaDocument23, DecryptedMessageMediaAudio8, DecryptedMessageMediaVideo23, DecryptedMessageMediaAudio, DecryptedMessageMediaExternalDocument, DecryptedMessageMediaPhoto, DecryptedMessageMediaVideo, DecryptedMessageMediaDocument, DecryptedMessageMediaVenue, DecryptedMessageMediaWebPage.
        """
        self.thumb = thumb
        self.thumb_w = thumb_w
        self.thumb_h = thumb_h
        self.w = w
        self.h = h
        self.size = size
        self.key = key
        self.iv = iv
        self.caption = caption

    def to_dict(self):
        return {
            '_': 'DecryptedMessageMediaPhoto',
            'thumb': self.thumb,
            'thumb_w': self.thumb_w,
            'thumb_h': self.thumb_h,
            'w': self.w,
            'h': self.h,
            'size': self.size,
            'key': self.key,
            'iv': self.iv,
            'caption': self.caption
        }

    def __bytes__(self):
        return b''.join((
            b'x\x8d\xfa\xf1',
            self.serialize_bytes(self.thumb),
            struct.pack('<i', self.thumb_w),
            struct.pack('<i', self.thumb_h),
            struct.pack('<i', self.w),
            struct.pack('<i', self.h),
            struct.pack('<i', self.size),
            self.serialize_bytes(self.key),
            self.serialize_bytes(self.iv),
            self.serialize_bytes(self.caption),
        ))

    @classmethod
    def from_reader(cls, reader):
        _thumb = reader.tgread_bytes()
        _thumb_w = reader.read_int()
        _thumb_h = reader.read_int()
        _w = reader.read_int()
        _h = reader.read_int()
        _size = reader.read_int()
        _key = reader.tgread_bytes()
        _iv = reader.tgread_bytes()
        _caption = reader.tgread_string()
        return cls(thumb=_thumb, thumb_w=_thumb_w, thumb_h=_thumb_h, w=_w, h=_h, size=_size, key=_key, iv=_iv,
                   caption=_caption)


class DecryptedMessageMediaPhoto23(TLObject):
    CONSTRUCTOR_ID = 0x32798a8c
    SUBCLASS_OF_ID = 0x96a0e005

    def __init__(self, thumb: bytes, thumb_w: int, thumb_h: int, w: int, h: int, size: int, key: bytes, iv: bytes):
        """
        Constructor for secret.DecryptedMessageMedia: Instance of either DecryptedMessageMediaEmpty, DecryptedMessageMediaPhoto23, DecryptedMessageMediaVideo8, DecryptedMessageMediaGeoPoint, DecryptedMessageMediaContact, DecryptedMessageMediaDocument23, DecryptedMessageMediaAudio8, DecryptedMessageMediaVideo23, DecryptedMessageMediaAudio, DecryptedMessageMediaExternalDocument, DecryptedMessageMediaPhoto, DecryptedMessageMediaVideo, DecryptedMessageMediaDocument, DecryptedMessageMediaVenue, DecryptedMessageMediaWebPage.
        """
        self.thumb = thumb
        self.thumb_w = thumb_w
        self.thumb_h = thumb_h
        self.w = w
        self.h = h
        self.size = size
        self.key = key
        self.iv = iv

    def to_dict(self):
        return {
            '_': 'DecryptedMessageMediaPhoto23',
            'thumb': self.thumb,
            'thumb_w': self.thumb_w,
            'thumb_h': self.thumb_h,
            'w': self.w,
            'h': self.h,
            'size': self.size,
            'key': self.key,
            'iv': self.iv
        }

    def __bytes__(self):
        return b''.join((
            b'\x8c\x8ay2',
            self.serialize_bytes(self.thumb),
            struct.pack('<i', self.thumb_w),
            struct.pack('<i', self.thumb_h),
            struct.pack('<i', self.w),
            struct.pack('<i', self.h),
            struct.pack('<i', self.size),
            self.serialize_bytes(self.key),
            self.serialize_bytes(self.iv),
        ))

    @classmethod
    def from_reader(cls, reader):
        _thumb = reader.tgread_bytes()
        _thumb_w = reader.read_int()
        _thumb_h = reader.read_int()
        _w = reader.read_int()
        _h = reader.read_int()
        _size = reader.read_int()
        _key = reader.tgread_bytes()
        _iv = reader.tgread_bytes()
        return cls(thumb=_thumb, thumb_w=_thumb_w, thumb_h=_thumb_h, w=_w, h=_h, size=_size, key=_key, iv=_iv)


class DecryptedMessageMediaVenue(TLObject):
    CONSTRUCTOR_ID = 0x8a0df56f
    SUBCLASS_OF_ID = 0x96a0e005

    def __init__(self, lat: float, long: float, title: str, address: str, provider: str, venue_id: str):
        """
        Constructor for secret.DecryptedMessageMedia: Instance of either DecryptedMessageMediaEmpty, DecryptedMessageMediaPhoto23, DecryptedMessageMediaVideo8, DecryptedMessageMediaGeoPoint, DecryptedMessageMediaContact, DecryptedMessageMediaDocument23, DecryptedMessageMediaAudio8, DecryptedMessageMediaVideo23, DecryptedMessageMediaAudio, DecryptedMessageMediaExternalDocument, DecryptedMessageMediaPhoto, DecryptedMessageMediaVideo, DecryptedMessageMediaDocument, DecryptedMessageMediaVenue, DecryptedMessageMediaWebPage.
        """
        self.lat = lat
        self.long = long
        self.title = title
        self.address = address
        self.provider = provider
        self.venue_id = venue_id

    def to_dict(self):
        return {
            '_': 'DecryptedMessageMediaVenue',
            'lat': self.lat,
            'long': self.long,
            'title': self.title,
            'address': self.address,
            'provider': self.provider,
            'venue_id': self.venue_id
        }

    def __bytes__(self):
        return b''.join((
            b'o\xf5\r\x8a',
            struct.pack('<d', self.lat),
            struct.pack('<d', self.long),
            self.serialize_bytes(self.title),
            self.serialize_bytes(self.address),
            self.serialize_bytes(self.provider),
            self.serialize_bytes(self.venue_id),
        ))

    @classmethod
    def from_reader(cls, reader):
        _lat = reader.read_double()
        _long = reader.read_double()
        _title = reader.tgread_string()
        _address = reader.tgread_string()
        _provider = reader.tgread_string()
        _venue_id = reader.tgread_string()
        return cls(lat=_lat, long=_long, title=_title, address=_address, provider=_provider, venue_id=_venue_id)


class DecryptedMessageMediaVideo(TLObject):
    CONSTRUCTOR_ID = 0x970c8c0e
    SUBCLASS_OF_ID = 0x96a0e005

    def __init__(self, thumb: bytes, thumb_w: int, thumb_h: int, duration: int, mime_type: str, w: int, h: int,
                 size: int, key: bytes, iv: bytes, caption: str):
        """
        Constructor for secret.DecryptedMessageMedia: Instance of either DecryptedMessageMediaEmpty, DecryptedMessageMediaPhoto23, DecryptedMessageMediaVideo8, DecryptedMessageMediaGeoPoint, DecryptedMessageMediaContact, DecryptedMessageMediaDocument23, DecryptedMessageMediaAudio8, DecryptedMessageMediaVideo23, DecryptedMessageMediaAudio, DecryptedMessageMediaExternalDocument, DecryptedMessageMediaPhoto, DecryptedMessageMediaVideo, DecryptedMessageMediaDocument, DecryptedMessageMediaVenue, DecryptedMessageMediaWebPage.
        """
        self.thumb = thumb
        self.thumb_w = thumb_w
        self.thumb_h = thumb_h
        self.duration = duration
        self.mime_type = mime_type
        self.w = w
        self.h = h
        self.size = size
        self.key = key
        self.iv = iv
        self.caption = caption

    def to_dict(self):
        return {
            '_': 'DecryptedMessageMediaVideo',
            'thumb': self.thumb,
            'thumb_w': self.thumb_w,
            'thumb_h': self.thumb_h,
            'duration': self.duration,
            'mime_type': self.mime_type,
            'w': self.w,
            'h': self.h,
            'size': self.size,
            'key': self.key,
            'iv': self.iv,
            'caption': self.caption
        }

    def __bytes__(self):
        return b''.join((
            b'\x0e\x8c\x0c\x97',
            self.serialize_bytes(self.thumb),
            struct.pack('<i', self.thumb_w),
            struct.pack('<i', self.thumb_h),
            struct.pack('<i', self.duration),
            self.serialize_bytes(self.mime_type),
            struct.pack('<i', self.w),
            struct.pack('<i', self.h),
            struct.pack('<i', self.size),
            self.serialize_bytes(self.key),
            self.serialize_bytes(self.iv),
            self.serialize_bytes(self.caption),
        ))

    @classmethod
    def from_reader(cls, reader):
        _thumb = reader.tgread_bytes()
        _thumb_w = reader.read_int()
        _thumb_h = reader.read_int()
        _duration = reader.read_int()
        _mime_type = reader.tgread_string()
        _w = reader.read_int()
        _h = reader.read_int()
        _size = reader.read_int()
        _key = reader.tgread_bytes()
        _iv = reader.tgread_bytes()
        _caption = reader.tgread_string()
        return cls(thumb=_thumb, thumb_w=_thumb_w, thumb_h=_thumb_h, duration=_duration, mime_type=_mime_type, w=_w,
                   h=_h, size=_size, key=_key, iv=_iv, caption=_caption)


class DecryptedMessageMediaVideo23(TLObject):
    CONSTRUCTOR_ID = 0x524a415d
    SUBCLASS_OF_ID = 0x96a0e005

    def __init__(self, thumb: bytes, thumb_w: int, thumb_h: int, duration: int, mime_type: str, w: int, h: int,
                 size: int, key: bytes, iv: bytes):
        """
        Constructor for secret.DecryptedMessageMedia: Instance of either DecryptedMessageMediaEmpty, DecryptedMessageMediaPhoto23, DecryptedMessageMediaVideo8, DecryptedMessageMediaGeoPoint, DecryptedMessageMediaContact, DecryptedMessageMediaDocument23, DecryptedMessageMediaAudio8, DecryptedMessageMediaVideo23, DecryptedMessageMediaAudio, DecryptedMessageMediaExternalDocument, DecryptedMessageMediaPhoto, DecryptedMessageMediaVideo, DecryptedMessageMediaDocument, DecryptedMessageMediaVenue, DecryptedMessageMediaWebPage.
        """
        self.thumb = thumb
        self.thumb_w = thumb_w
        self.thumb_h = thumb_h
        self.duration = duration
        self.mime_type = mime_type
        self.w = w
        self.h = h
        self.size = size
        self.key = key
        self.iv = iv

    def to_dict(self):
        return {
            '_': 'DecryptedMessageMediaVideo23',
            'thumb': self.thumb,
            'thumb_w': self.thumb_w,
            'thumb_h': self.thumb_h,
            'duration': self.duration,
            'mime_type': self.mime_type,
            'w': self.w,
            'h': self.h,
            'size': self.size,
            'key': self.key,
            'iv': self.iv
        }

    def __bytes__(self):
        return b''.join((
            b']AJR',
            self.serialize_bytes(self.thumb),
            struct.pack('<i', self.thumb_w),
            struct.pack('<i', self.thumb_h),
            struct.pack('<i', self.duration),
            self.serialize_bytes(self.mime_type),
            struct.pack('<i', self.w),
            struct.pack('<i', self.h),
            struct.pack('<i', self.size),
            self.serialize_bytes(self.key),
            self.serialize_bytes(self.iv),
        ))

    @classmethod
    def from_reader(cls, reader):
        _thumb = reader.tgread_bytes()
        _thumb_w = reader.read_int()
        _thumb_h = reader.read_int()
        _duration = reader.read_int()
        _mime_type = reader.tgread_string()
        _w = reader.read_int()
        _h = reader.read_int()
        _size = reader.read_int()
        _key = reader.tgread_bytes()
        _iv = reader.tgread_bytes()
        return cls(thumb=_thumb, thumb_w=_thumb_w, thumb_h=_thumb_h, duration=_duration, mime_type=_mime_type, w=_w,
                   h=_h, size=_size, key=_key, iv=_iv)


class DecryptedMessageMediaVideo8(TLObject):
    CONSTRUCTOR_ID = 0x4cee6ef3
    SUBCLASS_OF_ID = 0x96a0e005

    def __init__(self, thumb: bytes, thumb_w: int, thumb_h: int, duration: int, w: int, h: int, size: int, key: bytes,
                 iv: bytes):
        """
        Constructor for secret.DecryptedMessageMedia: Instance of either DecryptedMessageMediaEmpty, DecryptedMessageMediaPhoto23, DecryptedMessageMediaVideo8, DecryptedMessageMediaGeoPoint, DecryptedMessageMediaContact, DecryptedMessageMediaDocument23, DecryptedMessageMediaAudio8, DecryptedMessageMediaVideo23, DecryptedMessageMediaAudio, DecryptedMessageMediaExternalDocument, DecryptedMessageMediaPhoto, DecryptedMessageMediaVideo, DecryptedMessageMediaDocument, DecryptedMessageMediaVenue, DecryptedMessageMediaWebPage.
        """
        self.thumb = thumb
        self.thumb_w = thumb_w
        self.thumb_h = thumb_h
        self.duration = duration
        self.w = w
        self.h = h
        self.size = size
        self.key = key
        self.iv = iv

    def to_dict(self):
        return {
            '_': 'DecryptedMessageMediaVideo8',
            'thumb': self.thumb,
            'thumb_w': self.thumb_w,
            'thumb_h': self.thumb_h,
            'duration': self.duration,
            'w': self.w,
            'h': self.h,
            'size': self.size,
            'key': self.key,
            'iv': self.iv
        }

    def __bytes__(self):
        return b''.join((
            b'\xf3n\xeeL',
            self.serialize_bytes(self.thumb),
            struct.pack('<i', self.thumb_w),
            struct.pack('<i', self.thumb_h),
            struct.pack('<i', self.duration),
            struct.pack('<i', self.w),
            struct.pack('<i', self.h),
            struct.pack('<i', self.size),
            self.serialize_bytes(self.key),
            self.serialize_bytes(self.iv),
        ))

    @classmethod
    def from_reader(cls, reader):
        _thumb = reader.tgread_bytes()
        _thumb_w = reader.read_int()
        _thumb_h = reader.read_int()
        _duration = reader.read_int()
        _w = reader.read_int()
        _h = reader.read_int()
        _size = reader.read_int()
        _key = reader.tgread_bytes()
        _iv = reader.tgread_bytes()
        return cls(thumb=_thumb, thumb_w=_thumb_w, thumb_h=_thumb_h, duration=_duration, w=_w, h=_h, size=_size,
                   key=_key, iv=_iv)


class DecryptedMessageMediaWebPage(TLObject):
    CONSTRUCTOR_ID = 0xe50511d8
    SUBCLASS_OF_ID = 0x96a0e005

    def __init__(self, url: str):
        """
        Constructor for secret.DecryptedMessageMedia: Instance of either DecryptedMessageMediaEmpty, DecryptedMessageMediaPhoto23, DecryptedMessageMediaVideo8, DecryptedMessageMediaGeoPoint, DecryptedMessageMediaContact, DecryptedMessageMediaDocument23, DecryptedMessageMediaAudio8, DecryptedMessageMediaVideo23, DecryptedMessageMediaAudio, DecryptedMessageMediaExternalDocument, DecryptedMessageMediaPhoto, DecryptedMessageMediaVideo, DecryptedMessageMediaDocument, DecryptedMessageMediaVenue, DecryptedMessageMediaWebPage.
        """
        self.url = url

    def to_dict(self):
        return {
            '_': 'DecryptedMessageMediaWebPage',
            'url': self.url
        }

    def __bytes__(self):
        return b''.join((
            b'\xd8\x11\x05\xe5',
            self.serialize_bytes(self.url),
        ))

    @classmethod
    def from_reader(cls, reader):
        _url = reader.tgread_string()
        return cls(url=_url)


class DecryptedMessageService(TLObject):
    CONSTRUCTOR_ID = 0x73164160
    SUBCLASS_OF_ID = 0x5182c3e8

    def __init__(self, action: 'TypeDecryptedMessageAction', random_id: int = None):
        """
        Constructor for secret.DecryptedMessage: Instance of either DecryptedMessage8, DecryptedMessageService8, DecryptedMessage23, DecryptedMessageService, DecryptedMessage46, DecryptedMessage.
        """
        self.action = action
        self.random_id = random_id if random_id is not None else int.from_bytes(os.urandom(8), 'big', signed=True)

    def to_dict(self):
        return {
            '_': 'DecryptedMessageService',
            'action': self.action.to_dict() if isinstance(self.action, TLObject) else self.action,
            'random_id': self.random_id
        }

    def __bytes__(self):
        return b''.join((
            b'`A\x16s',
            struct.pack('<q', self.random_id),
            bytes(self.action),
        ))

    @classmethod
    def from_reader(cls, reader):
        _random_id = reader.read_long()
        _action = reader.tgread_object()
        return cls(action=_action, random_id=_random_id)


class DecryptedMessageService8(TLObject):
    CONSTRUCTOR_ID = 0xaa48327d
    SUBCLASS_OF_ID = 0x5182c3e8

    def __init__(self, random_bytes: bytes, action: 'TypeDecryptedMessageAction', random_id: int = None):
        """
        Constructor for secret.DecryptedMessage: Instance of either DecryptedMessage8, DecryptedMessageService8, DecryptedMessage23, DecryptedMessageService, DecryptedMessage46, DecryptedMessage.
        """
        self.random_bytes = random_bytes
        self.action = action
        self.random_id = random_id if random_id is not None else int.from_bytes(os.urandom(8), 'big', signed=True)

    def to_dict(self):
        return {
            '_': 'DecryptedMessageService8',
            'random_bytes': self.random_bytes,
            'action': self.action.to_dict() if isinstance(self.action, TLObject) else self.action,
            'random_id': self.random_id
        }

    def __bytes__(self):
        return b''.join((
            b'}2H\xaa',
            struct.pack('<q', self.random_id),
            self.serialize_bytes(self.random_bytes),
            bytes(self.action),
        ))

    @classmethod
    def from_reader(cls, reader):
        _random_id = reader.read_long()
        _random_bytes = reader.tgread_bytes()
        _action = reader.tgread_object()
        return cls(random_bytes=_random_bytes, action=_action, random_id=_random_id)


class DocumentAttributeAnimated(TLObject):
    CONSTRUCTOR_ID = 0x11b58939
    SUBCLASS_OF_ID = 0x989b1da0

    def to_dict(self):
        return {
            '_': 'DocumentAttributeAnimated'
        }

    def __bytes__(self):
        return b''.join((
            b'9\x89\xb5\x11',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class DocumentAttributeAudio(TLObject):
    CONSTRUCTOR_ID = 0x9852f9c6
    SUBCLASS_OF_ID = 0x989b1da0

    def __init__(self, duration: int, voice: Optional[bool] = None, title: Optional[str] = None,
                 performer: Optional[str] = None, waveform: Optional[bytes] = None):
        """
        Constructor for secret.DocumentAttribute: Instance of either DocumentAttributeImageSize, DocumentAttributeAnimated, DocumentAttributeSticker23, DocumentAttributeVideo, DocumentAttributeAudio23, DocumentAttributeFilename, DocumentAttributeAudio45, DocumentAttributeSticker, DocumentAttributeAudio, DocumentAttributeVideo66.
        """
        self.duration = duration
        self.voice = voice
        self.title = title
        self.performer = performer
        self.waveform = waveform

    def to_dict(self):
        return {
            '_': 'DocumentAttributeAudio',
            'duration': self.duration,
            'voice': self.voice,
            'title': self.title,
            'performer': self.performer,
            'waveform': self.waveform
        }

    def __bytes__(self):
        return b''.join((
            b'\xc6\xf9R\x98',
            struct.pack('<I', (0 if self.voice is None or self.voice is False else 1024) | (
                0 if self.title is None or self.title is False else 1) | (
                            0 if self.performer is None or self.performer is False else 2) | (
                            0 if self.waveform is None or self.waveform is False else 4)),
            struct.pack('<i', self.duration),
            b'' if self.title is None or self.title is False else (self.serialize_bytes(self.title)),
            b'' if self.performer is None or self.performer is False else (self.serialize_bytes(self.performer)),
            b'' if self.waveform is None or self.waveform is False else (self.serialize_bytes(self.waveform)),
        ))

    @classmethod
    def from_reader(cls, reader):
        flags = reader.read_int()

        _voice = bool(flags & 1024)
        _duration = reader.read_int()
        if flags & 1:
            _title = reader.tgread_string()
        else:
            _title = None
        if flags & 2:
            _performer = reader.tgread_string()
        else:
            _performer = None
        if flags & 4:
            _waveform = reader.tgread_bytes()
        else:
            _waveform = None
        return cls(duration=_duration, voice=_voice, title=_title, performer=_performer, waveform=_waveform)


class DocumentAttributeAudio23(TLObject):
    CONSTRUCTOR_ID = 0x51448e5
    SUBCLASS_OF_ID = 0x989b1da0

    def __init__(self, duration: int):
        """
        Constructor for secret.DocumentAttribute: Instance of either DocumentAttributeImageSize, DocumentAttributeAnimated, DocumentAttributeSticker23, DocumentAttributeVideo, DocumentAttributeAudio23, DocumentAttributeFilename, DocumentAttributeAudio45, DocumentAttributeSticker, DocumentAttributeAudio, DocumentAttributeVideo66.
        """
        self.duration = duration

    def to_dict(self):
        return {
            '_': 'DocumentAttributeAudio23',
            'duration': self.duration
        }

    def __bytes__(self):
        return b''.join((
            b'\xe5H\x14\x05',
            struct.pack('<i', self.duration),
        ))

    @classmethod
    def from_reader(cls, reader):
        _duration = reader.read_int()
        return cls(duration=_duration)


class DocumentAttributeAudio45(TLObject):
    CONSTRUCTOR_ID = 0xded218e0
    SUBCLASS_OF_ID = 0x989b1da0

    def __init__(self, duration: int, title: str, performer: str):
        """
        Constructor for secret.DocumentAttribute: Instance of either DocumentAttributeImageSize, DocumentAttributeAnimated, DocumentAttributeSticker23, DocumentAttributeVideo, DocumentAttributeAudio23, DocumentAttributeFilename, DocumentAttributeAudio45, DocumentAttributeSticker, DocumentAttributeAudio, DocumentAttributeVideo66.
        """
        self.duration = duration
        self.title = title
        self.performer = performer

    def to_dict(self):
        return {
            '_': 'DocumentAttributeAudio45',
            'duration': self.duration,
            'title': self.title,
            'performer': self.performer
        }

    def __bytes__(self):
        return b''.join((
            b'\xe0\x18\xd2\xde',
            struct.pack('<i', self.duration),
            self.serialize_bytes(self.title),
            self.serialize_bytes(self.performer),
        ))

    @classmethod
    def from_reader(cls, reader):
        _duration = reader.read_int()
        _title = reader.tgread_string()
        _performer = reader.tgread_string()
        return cls(duration=_duration, title=_title, performer=_performer)


class DocumentAttributeFilename(TLObject):
    CONSTRUCTOR_ID = 0x15590068
    SUBCLASS_OF_ID = 0x989b1da0

    def __init__(self, file_name: str):
        """
        Constructor for secret.DocumentAttribute: Instance of either DocumentAttributeImageSize, DocumentAttributeAnimated, DocumentAttributeSticker23, DocumentAttributeVideo, DocumentAttributeAudio23, DocumentAttributeFilename, DocumentAttributeAudio45, DocumentAttributeSticker, DocumentAttributeAudio, DocumentAttributeVideo66.
        """
        self.file_name = file_name

    def to_dict(self):
        return {
            '_': 'DocumentAttributeFilename',
            'file_name': self.file_name
        }

    def __bytes__(self):
        return b''.join((
            b'h\x00Y\x15',
            self.serialize_bytes(self.file_name),
        ))

    @classmethod
    def from_reader(cls, reader):
        _file_name = reader.tgread_string()
        return cls(file_name=_file_name)


class DocumentAttributeImageSize(TLObject):
    CONSTRUCTOR_ID = 0x6c37c15c
    SUBCLASS_OF_ID = 0x989b1da0

    def __init__(self, w: int, h: int):
        """
        Constructor for secret.DocumentAttribute: Instance of either DocumentAttributeImageSize, DocumentAttributeAnimated, DocumentAttributeSticker23, DocumentAttributeVideo, DocumentAttributeAudio23, DocumentAttributeFilename, DocumentAttributeAudio45, DocumentAttributeSticker, DocumentAttributeAudio, DocumentAttributeVideo66.
        """
        self.w = w
        self.h = h

    def to_dict(self):
        return {
            '_': 'DocumentAttributeImageSize',
            'w': self.w,
            'h': self.h
        }

    def __bytes__(self):
        return b''.join((
            b'\\\xc17l',
            struct.pack('<i', self.w),
            struct.pack('<i', self.h),
        ))

    @classmethod
    def from_reader(cls, reader):
        _w = reader.read_int()
        _h = reader.read_int()
        return cls(w=_w, h=_h)


class DocumentAttributeSticker(TLObject):
    CONSTRUCTOR_ID = 0x3a556302
    SUBCLASS_OF_ID = 0x989b1da0

    def __init__(self, alt: str, stickerset: 'TypeInputStickerSet'):
        """
        Constructor for secret.DocumentAttribute: Instance of either DocumentAttributeImageSize, DocumentAttributeAnimated, DocumentAttributeSticker23, DocumentAttributeVideo, DocumentAttributeAudio23, DocumentAttributeFilename, DocumentAttributeAudio45, DocumentAttributeSticker, DocumentAttributeAudio, DocumentAttributeVideo66.
        """
        self.alt = alt
        self.stickerset = stickerset

    def to_dict(self):
        return {
            '_': 'DocumentAttributeSticker',
            'alt': self.alt,
            'stickerset': self.stickerset.to_dict() if isinstance(self.stickerset, TLObject) else self.stickerset
        }

    def __bytes__(self):
        return b''.join((
            b'\x02cU:',
            self.serialize_bytes(self.alt),
            bytes(self.stickerset),
        ))

    @classmethod
    def from_reader(cls, reader):
        _alt = reader.tgread_string()
        _stickerset = reader.tgread_object()
        return cls(alt=_alt, stickerset=_stickerset)


class DocumentAttributeSticker23(TLObject):
    CONSTRUCTOR_ID = 0xfb0a5727
    SUBCLASS_OF_ID = 0x989b1da0

    def to_dict(self):
        return {
            '_': 'DocumentAttributeSticker23'
        }

    def __bytes__(self):
        return b''.join((
            b"'W\n\xfb",
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class DocumentAttributeVideo(TLObject):
    CONSTRUCTOR_ID = 0x5910cccb
    SUBCLASS_OF_ID = 0x989b1da0

    def __init__(self, duration: int, w: int, h: int):
        """
        Constructor for secret.DocumentAttribute: Instance of either DocumentAttributeImageSize, DocumentAttributeAnimated, DocumentAttributeSticker23, DocumentAttributeVideo, DocumentAttributeAudio23, DocumentAttributeFilename, DocumentAttributeAudio45, DocumentAttributeSticker, DocumentAttributeAudio, DocumentAttributeVideo66.
        """
        self.duration = duration
        self.w = w
        self.h = h

    def to_dict(self):
        return {
            '_': 'DocumentAttributeVideo',
            'duration': self.duration,
            'w': self.w,
            'h': self.h
        }

    def __bytes__(self):
        return b''.join((
            b'\xcb\xcc\x10Y',
            struct.pack('<i', self.duration),
            struct.pack('<i', self.w),
            struct.pack('<i', self.h),
        ))

    @classmethod
    def from_reader(cls, reader):
        _duration = reader.read_int()
        _w = reader.read_int()
        _h = reader.read_int()
        return cls(duration=_duration, w=_w, h=_h)


class DocumentAttributeVideo66(TLObject):
    CONSTRUCTOR_ID = 0xef02ce6
    SUBCLASS_OF_ID = 0x989b1da0

    def __init__(self, duration: int, w: int, h: int, round_message: Optional[bool] = None):
        """
        Constructor for secret.DocumentAttribute: Instance of either DocumentAttributeImageSize, DocumentAttributeAnimated, DocumentAttributeSticker23, DocumentAttributeVideo, DocumentAttributeAudio23, DocumentAttributeFilename, DocumentAttributeAudio45, DocumentAttributeSticker, DocumentAttributeAudio, DocumentAttributeVideo66.
        """
        self.duration = duration
        self.w = w
        self.h = h
        self.round_message = round_message

    def to_dict(self):
        return {
            '_': 'DocumentAttributeVideo66',
            'duration': self.duration,
            'w': self.w,
            'h': self.h,
            'round_message': self.round_message
        }

    def __bytes__(self):
        return b''.join((
            b'\xe6,\xf0\x0e',
            struct.pack('<I', (0 if self.round_message is None or self.round_message is False else 1)),
            struct.pack('<i', self.duration),
            struct.pack('<i', self.w),
            struct.pack('<i', self.h),
        ))

    @classmethod
    def from_reader(cls, reader):
        flags = reader.read_int()

        _round_message = bool(flags & 1)
        _duration = reader.read_int()
        _w = reader.read_int()
        _h = reader.read_int()
        return cls(duration=_duration, w=_w, h=_h, round_message=_round_message)


class FileLocation(TLObject):
    CONSTRUCTOR_ID = 0x53d69076
    SUBCLASS_OF_ID = 0x5ad8f388

    def __init__(self, dc_id: int, volume_id: int, local_id: int, secret: int):
        """
        Constructor for secret.FileLocation: Instance of either FileLocationUnavailable, FileLocation.
        """
        self.dc_id = dc_id
        self.volume_id = volume_id
        self.local_id = local_id
        self.secret = secret

    def to_dict(self):
        return {
            '_': 'FileLocation',
            'dc_id': self.dc_id,
            'volume_id': self.volume_id,
            'local_id': self.local_id,
            'secret': self.secret
        }

    def __bytes__(self):
        return b''.join((
            b'v\x90\xd6S',
            struct.pack('<i', self.dc_id),
            struct.pack('<q', self.volume_id),
            struct.pack('<i', self.local_id),
            struct.pack('<q', self.secret),
        ))

    @classmethod
    def from_reader(cls, reader):
        _dc_id = reader.read_int()
        _volume_id = reader.read_long()
        _local_id = reader.read_int()
        _secret = reader.read_long()
        return cls(dc_id=_dc_id, volume_id=_volume_id, local_id=_local_id, secret=_secret)


class FileLocationUnavailable(TLObject):
    CONSTRUCTOR_ID = 0x7c596b46
    SUBCLASS_OF_ID = 0x5ad8f388

    def __init__(self, volume_id: int, local_id: int, secret: int):
        """
        Constructor for secret.FileLocation: Instance of either FileLocationUnavailable, FileLocation.
        """
        self.volume_id = volume_id
        self.local_id = local_id
        self.secret = secret

    def to_dict(self):
        return {
            '_': 'FileLocationUnavailable',
            'volume_id': self.volume_id,
            'local_id': self.local_id,
            'secret': self.secret
        }

    def __bytes__(self):
        return b''.join((
            b'FkY|',
            struct.pack('<q', self.volume_id),
            struct.pack('<i', self.local_id),
            struct.pack('<q', self.secret),
        ))

    @classmethod
    def from_reader(cls, reader):
        _volume_id = reader.read_long()
        _local_id = reader.read_int()
        _secret = reader.read_long()
        return cls(volume_id=_volume_id, local_id=_local_id, secret=_secret)


class InputStickerSetEmpty(TLObject):
    CONSTRUCTOR_ID = 0xffb62b95
    SUBCLASS_OF_ID = 0xd1ea5569

    def to_dict(self):
        return {
            '_': 'InputStickerSetEmpty'
        }

    def __bytes__(self):
        return b''.join((
            b'\x95+\xb6\xff',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class InputStickerSetShortName(TLObject):
    CONSTRUCTOR_ID = 0x861cc8a0
    SUBCLASS_OF_ID = 0xd1ea5569

    def __init__(self, short_name: str):
        """
        Constructor for secret.InputStickerSet: Instance of either InputStickerSetShortName, InputStickerSetEmpty.
        """
        self.short_name = short_name

    def to_dict(self):
        return {
            '_': 'InputStickerSetShortName',
            'short_name': self.short_name
        }

    def __bytes__(self):
        return b''.join((
            b'\xa0\xc8\x1c\x86',
            self.serialize_bytes(self.short_name),
        ))

    @classmethod
    def from_reader(cls, reader):
        _short_name = reader.tgread_string()
        return cls(short_name=_short_name)


class MessageEntityBlockquote(TLObject):
    CONSTRUCTOR_ID = 0x20df5d0
    SUBCLASS_OF_ID = 0x8eaa4c27

    def __init__(self, offset: int, length: int):
        """
        Constructor for secret.MessageEntity: Instance of either MessageEntityUnknown, MessageEntityMention, MessageEntityHashtag, MessageEntityBotCommand, MessageEntityUrl, MessageEntityEmail, MessageEntityBold, MessageEntityItalic, MessageEntityCode, MessageEntityPre, MessageEntityTextUrl, MessageEntityMentionName, MessageEntityPhone, MessageEntityCashtag, MessageEntityUnderline, MessageEntityStrike, MessageEntityBlockquote.
        """
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityBlockquote',
            'offset': self.offset,
            'length': self.length
        }

    def __bytes__(self):
        return b''.join((
            b'\xd0\xf5\r\x02',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)


class MessageEntityBold(TLObject):
    CONSTRUCTOR_ID = 0xbd610bc9
    SUBCLASS_OF_ID = 0x8eaa4c27

    def __init__(self, offset: int, length: int):
        """
        Constructor for secret.MessageEntity: Instance of either MessageEntityUnknown, MessageEntityMention, MessageEntityHashtag, MessageEntityBotCommand, MessageEntityUrl, MessageEntityEmail, MessageEntityBold, MessageEntityItalic, MessageEntityCode, MessageEntityPre, MessageEntityTextUrl, MessageEntityMentionName, MessageEntityPhone, MessageEntityCashtag, MessageEntityUnderline, MessageEntityStrike, MessageEntityBlockquote.
        """
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityBold',
            'offset': self.offset,
            'length': self.length
        }

    def __bytes__(self):
        return b''.join((
            b'\xc9\x0ba\xbd',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)


class MessageEntityBotCommand(TLObject):
    CONSTRUCTOR_ID = 0x6cef8ac7
    SUBCLASS_OF_ID = 0x8eaa4c27

    def __init__(self, offset: int, length: int):
        """
        Constructor for secret.MessageEntity: Instance of either MessageEntityUnknown, MessageEntityMention, MessageEntityHashtag, MessageEntityBotCommand, MessageEntityUrl, MessageEntityEmail, MessageEntityBold, MessageEntityItalic, MessageEntityCode, MessageEntityPre, MessageEntityTextUrl, MessageEntityMentionName, MessageEntityPhone, MessageEntityCashtag, MessageEntityUnderline, MessageEntityStrike, MessageEntityBlockquote.
        """
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityBotCommand',
            'offset': self.offset,
            'length': self.length
        }

    def __bytes__(self):
        return b''.join((
            b'\xc7\x8a\xefl',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)


class MessageEntityCashtag(TLObject):
    CONSTRUCTOR_ID = 0x4c4e743f
    SUBCLASS_OF_ID = 0x8eaa4c27

    def __init__(self, offset: int, length: int):
        """
        Constructor for secret.MessageEntity: Instance of either MessageEntityUnknown, MessageEntityMention, MessageEntityHashtag, MessageEntityBotCommand, MessageEntityUrl, MessageEntityEmail, MessageEntityBold, MessageEntityItalic, MessageEntityCode, MessageEntityPre, MessageEntityTextUrl, MessageEntityMentionName, MessageEntityPhone, MessageEntityCashtag, MessageEntityUnderline, MessageEntityStrike, MessageEntityBlockquote.
        """
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityCashtag',
            'offset': self.offset,
            'length': self.length
        }

    def __bytes__(self):
        return b''.join((
            b'?tNL',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)


class MessageEntityCode(TLObject):
    CONSTRUCTOR_ID = 0x28a20571
    SUBCLASS_OF_ID = 0x8eaa4c27

    def __init__(self, offset: int, length: int):
        """
        Constructor for secret.MessageEntity: Instance of either MessageEntityUnknown, MessageEntityMention, MessageEntityHashtag, MessageEntityBotCommand, MessageEntityUrl, MessageEntityEmail, MessageEntityBold, MessageEntityItalic, MessageEntityCode, MessageEntityPre, MessageEntityTextUrl, MessageEntityMentionName, MessageEntityPhone, MessageEntityCashtag, MessageEntityUnderline, MessageEntityStrike, MessageEntityBlockquote.
        """
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityCode',
            'offset': self.offset,
            'length': self.length
        }

    def __bytes__(self):
        return b''.join((
            b'q\x05\xa2(',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)


class MessageEntityEmail(TLObject):
    CONSTRUCTOR_ID = 0x64e475c2
    SUBCLASS_OF_ID = 0x8eaa4c27

    def __init__(self, offset: int, length: int):
        """
        Constructor for secret.MessageEntity: Instance of either MessageEntityUnknown, MessageEntityMention, MessageEntityHashtag, MessageEntityBotCommand, MessageEntityUrl, MessageEntityEmail, MessageEntityBold, MessageEntityItalic, MessageEntityCode, MessageEntityPre, MessageEntityTextUrl, MessageEntityMentionName, MessageEntityPhone, MessageEntityCashtag, MessageEntityUnderline, MessageEntityStrike, MessageEntityBlockquote.
        """
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityEmail',
            'offset': self.offset,
            'length': self.length
        }

    def __bytes__(self):
        return b''.join((
            b'\xc2u\xe4d',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)


class MessageEntityHashtag(TLObject):
    CONSTRUCTOR_ID = 0x6f635b0d
    SUBCLASS_OF_ID = 0x8eaa4c27

    def __init__(self, offset: int, length: int):
        """
        Constructor for secret.MessageEntity: Instance of either MessageEntityUnknown, MessageEntityMention, MessageEntityHashtag, MessageEntityBotCommand, MessageEntityUrl, MessageEntityEmail, MessageEntityBold, MessageEntityItalic, MessageEntityCode, MessageEntityPre, MessageEntityTextUrl, MessageEntityMentionName, MessageEntityPhone, MessageEntityCashtag, MessageEntityUnderline, MessageEntityStrike, MessageEntityBlockquote.
        """
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityHashtag',
            'offset': self.offset,
            'length': self.length
        }

    def __bytes__(self):
        return b''.join((
            b'\r[co',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)


class MessageEntityItalic(TLObject):
    CONSTRUCTOR_ID = 0x826f8b60
    SUBCLASS_OF_ID = 0x8eaa4c27

    def __init__(self, offset: int, length: int):
        """
        Constructor for secret.MessageEntity: Instance of either MessageEntityUnknown, MessageEntityMention, MessageEntityHashtag, MessageEntityBotCommand, MessageEntityUrl, MessageEntityEmail, MessageEntityBold, MessageEntityItalic, MessageEntityCode, MessageEntityPre, MessageEntityTextUrl, MessageEntityMentionName, MessageEntityPhone, MessageEntityCashtag, MessageEntityUnderline, MessageEntityStrike, MessageEntityBlockquote.
        """
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityItalic',
            'offset': self.offset,
            'length': self.length
        }

    def __bytes__(self):
        return b''.join((
            b'`\x8bo\x82',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)


class MessageEntityMention(TLObject):
    CONSTRUCTOR_ID = 0xfa04579d
    SUBCLASS_OF_ID = 0x8eaa4c27

    def __init__(self, offset: int, length: int):
        """
        Constructor for secret.MessageEntity: Instance of either MessageEntityUnknown, MessageEntityMention, MessageEntityHashtag, MessageEntityBotCommand, MessageEntityUrl, MessageEntityEmail, MessageEntityBold, MessageEntityItalic, MessageEntityCode, MessageEntityPre, MessageEntityTextUrl, MessageEntityMentionName, MessageEntityPhone, MessageEntityCashtag, MessageEntityUnderline, MessageEntityStrike, MessageEntityBlockquote.
        """
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityMention',
            'offset': self.offset,
            'length': self.length
        }

    def __bytes__(self):
        return b''.join((
            b'\x9dW\x04\xfa',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)


class MessageEntityMentionName(TLObject):
    CONSTRUCTOR_ID = 0x352dca58
    SUBCLASS_OF_ID = 0x8eaa4c27

    def __init__(self, offset: int, length: int, user_id: int):
        """
        Constructor for secret.MessageEntity: Instance of either MessageEntityUnknown, MessageEntityMention, MessageEntityHashtag, MessageEntityBotCommand, MessageEntityUrl, MessageEntityEmail, MessageEntityBold, MessageEntityItalic, MessageEntityCode, MessageEntityPre, MessageEntityTextUrl, MessageEntityMentionName, MessageEntityPhone, MessageEntityCashtag, MessageEntityUnderline, MessageEntityStrike, MessageEntityBlockquote.
        """
        self.offset = offset
        self.length = length
        self.user_id = user_id

    def to_dict(self):
        return {
            '_': 'MessageEntityMentionName',
            'offset': self.offset,
            'length': self.length,
            'user_id': self.user_id
        }

    def __bytes__(self):
        return b''.join((
            b'X\xca-5',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
            struct.pack('<i', self.user_id),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        _user_id = reader.read_int()
        return cls(offset=_offset, length=_length, user_id=_user_id)


class MessageEntityPhone(TLObject):
    CONSTRUCTOR_ID = 0x9b69e34b
    SUBCLASS_OF_ID = 0x8eaa4c27

    def __init__(self, offset: int, length: int):
        """
        Constructor for secret.MessageEntity: Instance of either MessageEntityUnknown, MessageEntityMention, MessageEntityHashtag, MessageEntityBotCommand, MessageEntityUrl, MessageEntityEmail, MessageEntityBold, MessageEntityItalic, MessageEntityCode, MessageEntityPre, MessageEntityTextUrl, MessageEntityMentionName, MessageEntityPhone, MessageEntityCashtag, MessageEntityUnderline, MessageEntityStrike, MessageEntityBlockquote.
        """
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityPhone',
            'offset': self.offset,
            'length': self.length
        }

    def __bytes__(self):
        return b''.join((
            b'K\xe3i\x9b',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)


class MessageEntityPre(TLObject):
    CONSTRUCTOR_ID = 0x73924be0
    SUBCLASS_OF_ID = 0x8eaa4c27

    def __init__(self, offset: int, length: int, language: str):
        """
        Constructor for secret.MessageEntity: Instance of either MessageEntityUnknown, MessageEntityMention, MessageEntityHashtag, MessageEntityBotCommand, MessageEntityUrl, MessageEntityEmail, MessageEntityBold, MessageEntityItalic, MessageEntityCode, MessageEntityPre, MessageEntityTextUrl, MessageEntityMentionName, MessageEntityPhone, MessageEntityCashtag, MessageEntityUnderline, MessageEntityStrike, MessageEntityBlockquote.
        """
        self.offset = offset
        self.length = length
        self.language = language

    def to_dict(self):
        return {
            '_': 'MessageEntityPre',
            'offset': self.offset,
            'length': self.length,
            'language': self.language
        }

    def __bytes__(self):
        return b''.join((
            b'\xe0K\x92s',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
            self.serialize_bytes(self.language),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        _language = reader.tgread_string()
        return cls(offset=_offset, length=_length, language=_language)


class MessageEntityStrike(TLObject):
    CONSTRUCTOR_ID = 0xbf0693d4
    SUBCLASS_OF_ID = 0x8eaa4c27

    def __init__(self, offset: int, length: int):
        """
        Constructor for secret.MessageEntity: Instance of either MessageEntityUnknown, MessageEntityMention, MessageEntityHashtag, MessageEntityBotCommand, MessageEntityUrl, MessageEntityEmail, MessageEntityBold, MessageEntityItalic, MessageEntityCode, MessageEntityPre, MessageEntityTextUrl, MessageEntityMentionName, MessageEntityPhone, MessageEntityCashtag, MessageEntityUnderline, MessageEntityStrike, MessageEntityBlockquote.
        """
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityStrike',
            'offset': self.offset,
            'length': self.length
        }

    def __bytes__(self):
        return b''.join((
            b'\xd4\x93\x06\xbf',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)


class MessageEntityTextUrl(TLObject):
    CONSTRUCTOR_ID = 0x76a6d327
    SUBCLASS_OF_ID = 0x8eaa4c27

    def __init__(self, offset: int, length: int, url: str):
        """
        Constructor for secret.MessageEntity: Instance of either MessageEntityUnknown, MessageEntityMention, MessageEntityHashtag, MessageEntityBotCommand, MessageEntityUrl, MessageEntityEmail, MessageEntityBold, MessageEntityItalic, MessageEntityCode, MessageEntityPre, MessageEntityTextUrl, MessageEntityMentionName, MessageEntityPhone, MessageEntityCashtag, MessageEntityUnderline, MessageEntityStrike, MessageEntityBlockquote.
        """
        self.offset = offset
        self.length = length
        self.url = url

    def to_dict(self):
        return {
            '_': 'MessageEntityTextUrl',
            'offset': self.offset,
            'length': self.length,
            'url': self.url
        }

    def __bytes__(self):
        return b''.join((
            b"'\xd3\xa6v",
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
            self.serialize_bytes(self.url),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        _url = reader.tgread_string()
        return cls(offset=_offset, length=_length, url=_url)


class MessageEntityUnderline(TLObject):
    CONSTRUCTOR_ID = 0x9c4e7e8b
    SUBCLASS_OF_ID = 0x8eaa4c27

    def __init__(self, offset: int, length: int):
        """
        Constructor for secret.MessageEntity: Instance of either MessageEntityUnknown, MessageEntityMention, MessageEntityHashtag, MessageEntityBotCommand, MessageEntityUrl, MessageEntityEmail, MessageEntityBold, MessageEntityItalic, MessageEntityCode, MessageEntityPre, MessageEntityTextUrl, MessageEntityMentionName, MessageEntityPhone, MessageEntityCashtag, MessageEntityUnderline, MessageEntityStrike, MessageEntityBlockquote.
        """
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityUnderline',
            'offset': self.offset,
            'length': self.length
        }

    def __bytes__(self):
        return b''.join((
            b'\x8b~N\x9c',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)


class MessageEntityUnknown(TLObject):
    CONSTRUCTOR_ID = 0xbb92ba95
    SUBCLASS_OF_ID = 0x8eaa4c27

    def __init__(self, offset: int, length: int):
        """
        Constructor for secret.MessageEntity: Instance of either MessageEntityUnknown, MessageEntityMention, MessageEntityHashtag, MessageEntityBotCommand, MessageEntityUrl, MessageEntityEmail, MessageEntityBold, MessageEntityItalic, MessageEntityCode, MessageEntityPre, MessageEntityTextUrl, MessageEntityMentionName, MessageEntityPhone, MessageEntityCashtag, MessageEntityUnderline, MessageEntityStrike, MessageEntityBlockquote.
        """
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityUnknown',
            'offset': self.offset,
            'length': self.length
        }

    def __bytes__(self):
        return b''.join((
            b'\x95\xba\x92\xbb',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)


class MessageEntityUrl(TLObject):
    CONSTRUCTOR_ID = 0x6ed02538
    SUBCLASS_OF_ID = 0x8eaa4c27

    def __init__(self, offset: int, length: int):
        """
        Constructor for secret.MessageEntity: Instance of either MessageEntityUnknown, MessageEntityMention, MessageEntityHashtag, MessageEntityBotCommand, MessageEntityUrl, MessageEntityEmail, MessageEntityBold, MessageEntityItalic, MessageEntityCode, MessageEntityPre, MessageEntityTextUrl, MessageEntityMentionName, MessageEntityPhone, MessageEntityCashtag, MessageEntityUnderline, MessageEntityStrike, MessageEntityBlockquote.
        """
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityUrl',
            'offset': self.offset,
            'length': self.length
        }

    def __bytes__(self):
        return b''.join((
            b'8%\xd0n',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)


class PhotoCachedSize(TLObject):
    CONSTRUCTOR_ID = 0xe9a734fa
    SUBCLASS_OF_ID = 0x1fe3e096

    # noinspection PyShadowingBuiltins
    def __init__(self, type: str, location: 'TypeFileLocation', w: int, h: int, bytes: bytes):
        """
        Constructor for secret.PhotoSize: Instance of either PhotoSizeEmpty, PhotoSize, PhotoCachedSize.
        """
        self.type = type
        self.location = location
        self.w = w
        self.h = h
        self.bytes = bytes

    def to_dict(self):
        return {
            '_': 'PhotoCachedSize',
            'type': self.type,
            'location': self.location.to_dict() if isinstance(self.location, TLObject) else self.location,
            'w': self.w,
            'h': self.h,
            'bytes': self.bytes
        }

    def __bytes__(self):
        return b''.join((
            b'\xfa4\xa7\xe9',
            self.serialize_bytes(self.type),
            bytes(self.location),
            struct.pack('<i', self.w),
            struct.pack('<i', self.h),
            self.serialize_bytes(self.bytes),
        ))

    @classmethod
    def from_reader(cls, reader):
        _type = reader.tgread_string()
        _location = reader.tgread_object()
        _w = reader.read_int()
        _h = reader.read_int()
        _bytes = reader.tgread_bytes()
        return cls(type=_type, location=_location, w=_w, h=_h, bytes=_bytes)


class PhotoSize(TLObject):
    CONSTRUCTOR_ID = 0x77bfb61b
    SUBCLASS_OF_ID = 0x1fe3e096

    # noinspection PyShadowingBuiltins
    def __init__(self, type: str, location: 'TypeFileLocation', w: int, h: int, size: int):
        """
        Constructor for secret.PhotoSize: Instance of either PhotoSizeEmpty, PhotoSize, PhotoCachedSize.
        """
        self.type = type
        self.location = location
        self.w = w
        self.h = h
        self.size = size

    def to_dict(self):
        return {
            '_': 'PhotoSize',
            'type': self.type,
            'location': self.location.to_dict() if isinstance(self.location, TLObject) else self.location,
            'w': self.w,
            'h': self.h,
            'size': self.size
        }

    def __bytes__(self):
        return b''.join((
            b'\x1b\xb6\xbfw',
            self.serialize_bytes(self.type),
            bytes(self.location),
            struct.pack('<i', self.w),
            struct.pack('<i', self.h),
            struct.pack('<i', self.size),
        ))

    @classmethod
    def from_reader(cls, reader):
        _type = reader.tgread_string()
        _location = reader.tgread_object()
        _w = reader.read_int()
        _h = reader.read_int()
        _size = reader.read_int()
        return cls(type=_type, location=_location, w=_w, h=_h, size=_size)


class PhotoSizeEmpty(TLObject):
    CONSTRUCTOR_ID = 0xe17e23c
    SUBCLASS_OF_ID = 0x1fe3e096

    # noinspection PyShadowingBuiltins
    def __init__(self, type: str):
        """
        Constructor for secret.PhotoSize: Instance of either PhotoSizeEmpty, PhotoSize, PhotoCachedSize.
        """
        self.type = type

    def to_dict(self):
        return {
            '_': 'PhotoSizeEmpty',
            'type': self.type
        }

    def __bytes__(self):
        return b''.join((
            b'<\xe2\x17\x0e',
            self.serialize_bytes(self.type),
        ))

    @classmethod
    def from_reader(cls, reader):
        _type = reader.tgread_string()
        return cls(type=_type)


class SendMessageCancelAction(TLObject):
    CONSTRUCTOR_ID = 0xfd5ec8f5
    SUBCLASS_OF_ID = 0x4f003a1a

    def to_dict(self):
        return {
            '_': 'SendMessageCancelAction'
        }

    def __bytes__(self):
        return b''.join((
            b'\xf5\xc8^\xfd',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class SendMessageChooseContactAction(TLObject):
    CONSTRUCTOR_ID = 0x628cbc6f
    SUBCLASS_OF_ID = 0x4f003a1a

    def to_dict(self):
        return {
            '_': 'SendMessageChooseContactAction'
        }

    def __bytes__(self):
        return b''.join((
            b'o\xbc\x8cb',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class SendMessageGeoLocationAction(TLObject):
    CONSTRUCTOR_ID = 0x176f8ba1
    SUBCLASS_OF_ID = 0x4f003a1a

    def to_dict(self):
        return {
            '_': 'SendMessageGeoLocationAction'
        }

    def __bytes__(self):
        return b''.join((
            b'\xa1\x8bo\x17',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class SendMessageRecordAudioAction(TLObject):
    CONSTRUCTOR_ID = 0xd52f73f7
    SUBCLASS_OF_ID = 0x4f003a1a

    def to_dict(self):
        return {
            '_': 'SendMessageRecordAudioAction'
        }

    def __bytes__(self):
        return b''.join((
            b'\xf7s/\xd5',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class SendMessageRecordRoundAction(TLObject):
    CONSTRUCTOR_ID = 0x88f27fbc
    SUBCLASS_OF_ID = 0x4f003a1a

    def to_dict(self):
        return {
            '_': 'SendMessageRecordRoundAction'
        }

    def __bytes__(self):
        return b''.join((
            b'\xbc\x7f\xf2\x88',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class SendMessageRecordVideoAction(TLObject):
    CONSTRUCTOR_ID = 0xa187d66f
    SUBCLASS_OF_ID = 0x4f003a1a

    def to_dict(self):
        return {
            '_': 'SendMessageRecordVideoAction'
        }

    def __bytes__(self):
        return b''.join((
            b'o\xd6\x87\xa1',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class SendMessageTypingAction(TLObject):
    CONSTRUCTOR_ID = 0x16bf744e
    SUBCLASS_OF_ID = 0x4f003a1a

    def to_dict(self):
        return {
            '_': 'SendMessageTypingAction'
        }

    def __bytes__(self):
        return b''.join((
            b'Nt\xbf\x16',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class SendMessageUploadAudioAction(TLObject):
    CONSTRUCTOR_ID = 0xe6ac8a6f
    SUBCLASS_OF_ID = 0x4f003a1a

    def to_dict(self):
        return {
            '_': 'SendMessageUploadAudioAction'
        }

    def __bytes__(self):
        return b''.join((
            b'o\x8a\xac\xe6',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class SendMessageUploadDocumentAction(TLObject):
    CONSTRUCTOR_ID = 0x8faee98e
    SUBCLASS_OF_ID = 0x4f003a1a

    def to_dict(self):
        return {
            '_': 'SendMessageUploadDocumentAction'
        }

    def __bytes__(self):
        return b''.join((
            b'\x8e\xe9\xae\x8f',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class SendMessageUploadPhotoAction(TLObject):
    CONSTRUCTOR_ID = 0x990a3c1a
    SUBCLASS_OF_ID = 0x4f003a1a

    def to_dict(self):
        return {
            '_': 'SendMessageUploadPhotoAction'
        }

    def __bytes__(self):
        return b''.join((
            b'\x1a<\n\x99',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class SendMessageUploadRoundAction(TLObject):
    CONSTRUCTOR_ID = 0xbb718624
    SUBCLASS_OF_ID = 0x4f003a1a

    def to_dict(self):
        return {
            '_': 'SendMessageUploadRoundAction'
        }

    def __bytes__(self):
        return b''.join((
            b'$\x86q\xbb',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class SendMessageUploadVideoAction(TLObject):
    CONSTRUCTOR_ID = 0x92042ff7
    SUBCLASS_OF_ID = 0x4f003a1a

    def to_dict(self):
        return {
            '_': 'SendMessageUploadVideoAction'
        }

    def __bytes__(self):
        return b''.join((
            b'\xf7/\x04\x92',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()
