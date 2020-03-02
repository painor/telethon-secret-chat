# telethon-secret-chat
Secret chat plugin for telethon

This is still a work in progress so expect more commits to it. 
Used https://core.telegram.org/api/end-to-end at first but it wasn't clear enough so I followed their advice and checked one of the implementations that had it https://github.com/danog/MadelineProto so this pluigin is based on daniil's implementation at its core.

- [x] Accepting secret chats  
- [x] Creating secret chats 
- [x] Closing secret chats 
- [x] Sending text messages 
- [x]  Recieving text messages 
- [x] Uploading/downloading media 
- [x] Dealing with rekeying¹
- [ ] Saving secret chats keys to database²
- [ ] Saving messages to database³
- [ ] Automatic decryption/accepting/finishing⁴

¹ Every 100 messages you need to recreate the auth key.

² Auth keys are saved client sides so if you restart the script you will lose all secret chats you had and can no longer recieve messages from them

³ There is no get_messages function in secret chats so users can't see old messages.

⁴ Since event building are sync we currently can't decrypt implitctly and the user has to do it themselves.


Examples : 

```

soon

```

