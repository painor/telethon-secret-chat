from abc import ABC, abstractmethod


class SecretSession(ABC):
    def __init__(self):
        pass



    @property
    @abstractmethod
    def temp_secret_chat(self):
        """
        Returns a list of temporary ``Chats`` instance that are used
        to create and accept secret chats. (they will be deleted)
        """
        raise NotImplementedError

    @temp_secret_chat.setter
    @abstractmethod
    def temp_secret_chat(self, value):
        """
        Sets a list of temporary ``Chats`` instance that are used
        to create and accept secret chats. (they will be deleted)
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def secret_chats(self):
        """
        Returns a list of ``Chats`` instance that will be saved for
        future usage
        """
        raise NotImplementedError

    @secret_chats.setter
    @abstractmethod
    def secret_chats(self, value):
        """
        Sets a list of ``Chats`` instance
        """
        raise NotImplementedError

    @abstractmethod
    def close(self):
        """
        Should be used to free any used resources.
        Can be left empty if none.
        """

    @abstractmethod
    def save(self):
        """
        Called whenever important properties change. It should
        make persist the relevant session information to disk.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        """
        Should delete the stored information from disk since it's not valid anymore.
        """
        raise NotImplementedError
