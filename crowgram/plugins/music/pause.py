'''
Plugin Name: Pause
Developer: iniridwanul
License: AGPL-3.0 license
'''

import core.client
from os import environ
from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.contacts import GetContactsRequest
from pytgcalls.exceptions import GroupCallNotFound

crowgram_assistant = core.client.crowgram_assistant
call = core.client.crowgram_call
owner = int(environ["owner"])

@events.register(events.NewMessage(incoming=True, pattern=r"\>pause"))
async def pause_audio(event):
    try:
        await event.delete()
    except:
        pass
    chat_id = event.to_id.channel_id
    requestor_id = event.from_id.user_id
    get_user_details = await crowgram_assistant(GetFullUserRequest(requestor_id))
    first_name = get_user_details.users[0].first_name
    crowgram_assistant.parse_mode = "html"
    contacts = await crowgram_assistant(GetContactsRequest(hash=0))
    contacts_users_id = set([])
    for user in contacts.users:
        contacts_users_id.add(user.id)
    if owner == requestor_id or requestor_id in contacts_users_id:
        try:
            await call.pause_stream(chat_id)
            await crowgram_assistant.send_message(chat_id, f"▶️ Paused\n👤Order by: <a href='tg://user?id={requestor_id}'>{first_name}</a>")
        except GroupCallNotFound:
            await crowgram_assistant.send_message(chat_id, f"Dear <a href='tg://user?id={requestor_id}'>{first_name}</a>,\n❗️Streaming is not on, so pausing is not possible.")
        except:
            pass
    else:
        await crowgram_assistant.send_message(chat_id, f"Dear <a href='tg://user?id={requestor_id}'>{first_name}</a>,\n❗️You don't have permission to use me; please deploy your own Crowgram.")