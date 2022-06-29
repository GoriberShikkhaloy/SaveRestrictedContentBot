#Github.com/Vasusen-code

import time, os

from .. import bot as Drone
from .. import userbot, Bot
from .. import FORCESUB as fs
from main.plugins.pyroplug import get_msg
from main.plugins.helpers import get_link, join, screenshot

from telethon import events

from ethon.telefunc import force_sub

ft = f"এই বটটি ব্যবহার করার জন্য আপনাকে হুদাই @{fs} এই চ্যানেলে জয়েন হতে হবে।"

message = "আপনি যে লিংক থেকে কোনো ফাইল ডাউনলোড করে নিতে চান সেটির লিংক আমাকে দিন।"
          
# To-Do:
# Make these codes shorter and clean
# ofc will never do it. 

@Drone.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def clone(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        if reply.text == message:
            return
    try:
        link = get_link(event.text)
        if not link:
            return
    except TypeError:
        return
    s, r = await force_sub(event.client, fs, event.sender_id, ft)
    if s == True:
        await event.reply(r)
        return
    edit = await event.reply("প্রক্রিয়া চলছে...")
    if 't.me/+' in link:
        q = await join(userbot, link)
        await edit.edit(q)
        return 
    if 't.me/' in link:
        await get_msg(userbot, Bot, event.sender_id, edit.id, link, 0)
        
