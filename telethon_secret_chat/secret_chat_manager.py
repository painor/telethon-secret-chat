from enum import Enum

from telethon import TelegramClient
from telethon.tl import types

from telethon_secret_chat.secret_sechma import secret_tlobjects
from .secret_methods import SecretChatMethods


class SECRET_TYPES(Enum):
    accept = 1
    decrypt = 2


class SecretChatManager(SecretChatMethods):

    def __init__(self, client: TelegramClient, auto_accept=False):
        self.temp_secret_chat = {}
        self.secret_chats = {}
        self.secret_events = []
        self.dh_config = None
        self.auto_accept = auto_accept
        self.client = client
        self.patch_tlobjects()
        self.client.add_event_handler(self._secret_chat_event_loop)

    def add_secret_event_handler(self, event_type=SECRET_TYPES.decrypt, func=None):
        if event_type != SECRET_TYPES.decrypt and event_type != SECRET_TYPES.accept or not func:
            raise ValueError("Wrong params")
        # deal with patterns etc
        self.secret_events.append((event_type, func))

    def patch_tlobjects(self):
        from telethon.tl.alltlobjects import tlobjects
        tlobjects.update(secret_tlobjects)

    def patch_event(self, event):

        async def reply(message, ttl=0):
            return await self.send_secret_message(event.message.chat_id, message, ttl,
                                                  event.random_id)

        async def respond(message, ttl=0):
            return await self.send_secret_message(event.message.chat_id, message, ttl)

        event.reply = reply
        event.response = respond

    async def _secret_chat_event_loop(self, event):
        if isinstance(event, types.UpdateEncryption):
            if isinstance(event.chat, types.EncryptedChat):
                await self.finish_secret_chat_creation(event.chat)
            elif isinstance(event.chat, types.EncryptedChatRequested):
                if self.auto_accept:
                    await self.accept_secret_chat(event.chat)
                    return
                for event in self.secret_events:
                    (event, callback) = event
                    if event == SECRET_TYPES.accept:
                        self.client.loop.create_task(callback(event))
        elif isinstance(event, types.UpdateNewEncryptedMessage):
            decrypted_event = None
            for events in self.secret_events:
                (event_type, callback) = events
                if event_type == SECRET_TYPES.decrypt:
                    if not decrypted_event:
                        decrypted_event = await self.handle_encrypted_update(event)
                        self.patch_event(decrypted_event)
                    self.client.loop.create_task(callback(decrypted_event))
