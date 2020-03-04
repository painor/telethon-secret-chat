from .abstract import SecretSession


class SecretMemorySession(SecretSession):
    @property
    def temp_secret_chat(self):
        return self._temp_secret_chat

    @property
    def secret_chats(self):
        return self._secret_chats

    @temp_secret_chat.setter
    def temp_secret_chat(self, value):
        self._temp_secret_chat = value

    @secret_chats.setter
    def secret_chats(self, value):
        self._secret_chats = value

    @property
    def temp_rekeyed_secret_chats(self):
        return self._temp_rekeyed_secret_chats

    @temp_rekeyed_secret_chats.setter
    def temp_rekeyed_secret_chats(self, value):
        self._temp_rekeyed_secret_chats = value

    def __init__(self):
        super().__init__()
        self._temp_secret_chat = {}
        self._secret_chats = {}
        self._temp_rekeyed_secret_chats = {}

    def close(self):
        pass

    def save(self):
        pass

    def delete(self):
        pass
