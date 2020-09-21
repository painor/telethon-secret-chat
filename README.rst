telethon-secret-chat
====================

Secret chat plugin for telethon, `available on PyPi`_.

This is still a work in progress so expect more commits to it. Originally
based on the `End-to-End Encryption, Secret Chats`_ document, but it wasn't
clear enough so I followed their advice and checked one of the implementations
that had it (`MadelineProto`_). Therefore, this plugin is based on
`Daniil`_'s implementation at its core.

Features
--------

-  ☒ Accepting secret chats
-  ☒ Creating secret chats
-  ☒ Closing secret chats
-  ☒ Sending text messages
-  ☒ Recieving text messages
-  ☒ Uploading/downloading media
-  ☒ Dealing with rekeying [1]_
-  ☒ Saving secret chats keys to database [2]_
-  ☐ Saving messages to database [3]_
-  ☒ Automatic decryption/accepting/finishing
-  ☐ Compatibility with `tdlib`_ [4]_

.. [1] Every 100 messages you need to recreate the auth key.
.. [2] Auth keys are saved client sides so if you restart the script you will
       lose all secret chats you had and can no longer recieve messages from
       them.
.. [3] There is no ``get_messages`` function in secret chats so users can't see
       old messages.
.. [4] The secret chat implementation of `tdlib`_ differs from other clients,
       so applications like Telegram X or the mac client may not work with
       these chats.

Installation
------------

Easiest way is to install it through ``pip``

.. code-block:: sh

    pip install telethon-secret-chat~=0.2

Example
-------

.. code-block:: python

    from telethon import TelegramClient
    from telethon_secret_chat import SecretChatManager

    client = TelegramClient(...)

    async def replier(event):
        # all events are encrypted by default
        if event.decrypted_event.message and event.decrypted_event.message == "hello":
            await event.reply("**hi**") # parse_mode is markdown by default


    async def new_chat(chat, created_by_me):
        if created_by_me:
            print("User {} has accepted our secret chat request".format(chat))
        else:
            print("We have accepted the secret chat request of {}".format(chat))


    manager = SecretChatManager(client, auto_accept=True,
                                new_chat_created=new_chat)  # automatically accept new secret chats
    manager.add_secret_event_handler(func=replier)  # we can specify the type of the event

    with client:
        client.run_until_disconnected()

To start a secret chat you can call:

.. code-block:: python

    manager.start_secret_chat(target)

To use sqlite as a storage session you need to pass an sqlite connection to `SecretChatManager`:

.. code-block:: python

        manager = SecretChatManager(client, session=db_conn, auto_accept=True)
        # you can also pass client.session from telethon as such
        manager = SecretChatManager(client, session=client.session, auto_accept=True)

To manually accept incoming you can do as follow:

.. code-block:: python

        from telethon_secret_chat import SecretChatManager, SECRET_TYPES

        manager = SecretChatManager(client, auto_accept=False)
        manager.add_secret_event_handler(
            event_type=SECRET_TYPES.accept,
            func=accept_secret_chat_handler
        )

In your handler, you can do the following:

.. code-block:: python

    await manager.accept_secret_chat(event.chat)

.. _`available on PyPi`: https://pypi.org/project/telethon-secret-chat/
.. _`End-to-End Encryption, Secret Chats`: https://core.telegram.org/api/end-to-end
.. _`MadelineProto`: https://github.com/danog/MadelineProto
.. _`Daniil`: https://github.com/danog
.. _`tdlib`: https://telegram.org/blog/tdlib
