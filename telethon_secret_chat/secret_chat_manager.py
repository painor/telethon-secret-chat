import sqlite3
from enum import Enum
from typing import Callable

from telethon import TelegramClient
from telethon.sessions import SQLiteSession
from telethon.tl import types
from telethon.tl.alltlobjects import tlobjects
from .storage.abstract import SecretSession
from .storage.sqlite import SecretSQLiteSession
from .storage.memory import SecretMemorySession
from .secret_sechma import secret_tlobjects
from .secret_methods import SecretChatMethods


class SECRET_TYPES(Enum):
    accept = 1
    decrypt = 2


def patch_tlobjects():
    tlobjects.update(secret_tlobjects)


class SecretChatManager(SecretChatMethods):

    def __init__(self, client: TelegramClient, session: SecretSession = None, auto_accept: bool = False,
                 new_chat_created: callable = None):
        self.secret_events = []
        self.dh_config = None
        self.auto_accept = auto_accept
        self.client = client
        self.new_chat_created = new_chat_created
        if not session:
            self.session = SecretMemorySession()
        elif isinstance(session, sqlite3.Connection):
            self.session = SecretSQLiteSession(session)
        elif isinstance(session, SQLiteSession):
            self.session = SecretSQLiteSession(session._conn)
        else:
            self.session = session
        self.client.add_event_handler(self._secret_chat_event_loop)
        self._log = client._log["secret_chat"]

    def add_secret_event_handler(self, event_type=SECRET_TYPES.decrypt, func: Callable = None):
        if event_type != SECRET_TYPES.decrypt and event_type != SECRET_TYPES.accept or not func:
            raise ValueError("Wrong params")
        # deal with patterns etc
        self.secret_events.append((event_type, func))

    def patch_event(self, event, decrypted_event):

        async def reply(message: str, ttl: int = 0):
            return await self.send_secret_message(event.message.chat_id, message, ttl,
                                                  decrypted_event.random_id)

        async def respond(message: str, ttl: int = 0):
            return await self.send_secret_message(event.message.chat_id, message, ttl)

        event.decrypted_event = decrypted_event
        event.reply = reply
        event.respond = respond

    async def _secret_chat_event_loop(self, event):
        if 0x1be31789 not in tlobjects:  # check for decryptedMessage constructor
            patch_tlobjects()  # patch the tlobjects so we can read it with bytes

        if isinstance(event, types.UpdateEncryption):
            if isinstance(event.chat, types.EncryptedChat):

                await self.finish_secret_chat_creation(event.chat)
                if self.new_chat_created:
                    self.client.loop.create_task(self.new_chat_created(event.chat,created_by_me=True))
            elif isinstance(event.chat, types.EncryptedChatRequested):
                if self.auto_accept:
                    await self.accept_secret_chat(event.chat)
                    if self.new_chat_created:
                        self.client.loop.create_task(self.new_chat_created(event.chat, created_by_me=False))
                    return
                for events in self.secret_events:
                    (event_type, callback) = events
                    if event_type == SECRET_TYPES.accept:
                        self.client.loop.create_task(callback(event))
        elif isinstance(event, types.UpdateNewEncryptedMessage):
            decrypted_event = None
            for events in self.secret_events:
                (event_type, callback) = events
                if event_type == SECRET_TYPES.decrypt:
                    if not decrypted_event:
                        decrypted_event = await self.handle_encrypted_update(event)
                        if "DecryptedMessage" not in type(decrypted_event).__name__:
                            return

                        self.patch_event(event, decrypted_event)
                    self.client.loop.create_task(callback(event))
