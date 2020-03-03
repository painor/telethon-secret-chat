telethon-secret-chat
====================

Secret chat plugin for telethon

This is still a work in progress so expect more commits to it. Used
`https://core.telegram.org/api/end-to-end`_ at first but it wasn't clear
enough so I followed their advice and checked one of the implementations
that had it `https://github.com/danog/MadelineProto`_ so this pluigin is
based on daniil's implementation at its core.

-  ☒ Accepting secret chats
-  ☒ Creating secret chats
-  ☒ Closing secret chats
-  ☒ Sending text messages
-  ☒ Recieving text messages
-  ☒ Uploading/downloading media
-  ☒ Dealing with rekeying¹
-  ☐ Saving secret chats keys to database²
-  ☐ Saving messages to database³
-  ☒ Automatic decryption/accepting/finishing

¹ Every 100 messages you need to recreate the auth key.

² Auth keys are saved client sides so if you restart the script you will
lose all secret chats you had and can no longer recieve messages from
them

³ There is no get_messages function in secret chats so users can't see
old messages.

Examples :

::

   client = TelegramClient(...)

   async def replier(event):
    # all events are encrypted by default
    if event.decrypted_event.message and event.decrypted_event.message == "hello":
        await event.reply("hi")


    manager = SecretChatManager(client, auto_accept=True)  # automatically accept new secret chats
    manager.add_secret_event_handler(func=replier) # we can specify the type of the event
    client.run_until_disconnected()

.. _`https://core.telegram.org/api/end-to-end`: https://core.telegram.org/api/end-to-end
.. _`https://github.com/danog/MadelineProto`: https://github.com/danog/MadelineProto
