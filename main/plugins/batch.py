#Tg:MaheshChauhan/DroneBots
#Github.com/Vasusen-code

"""
Plugin for both public & private channels!
"""

import time, os, asyncio

from .. import bot as Drone
from .. import userbot, Bot, AUTH
from .. import FORCESUB as fs
from main.plugins.pyroplug import check, get_bulk_msg
from main.plugins.helpers import get_link, screenshot

from telethon import events, Button, errors
from telethon.tl.types import DocumentAttributeVideo

from pyrogram import Client 
from pyrogram.errors import FloodWait

from ethon.pyfunc import video_metadata
from ethon.telefunc import force_sub

ft = f"এই বটটি ব্যবহার করার জন্য আপনাকে হুদাই @{fs} এই চ্যানেলে জয়েন হতে হবে।"

batch = []

async def get_pvt_content(event, chat, id):
    msg = await userbot.get_messages(chat, ids=id)
    await event.client.send_message(event.chat_id, msg) 
    
@Drone.on(events.NewMessage(incoming=True, from_users=AUTH, pattern='/batch'))
async def _batch(event):
    if not event.is_private:
        return
    # wtf is the use of fsub here if the command is meant for the owner? 
    # well am too lazy to clean 
    s, r = await force_sub(event.client, fs, event.sender_id, ft) 
    if s == True:
        await event.reply(r)
        return       
    if f'{event.sender_id}' in batch:
        return await event.reply("আপনি ইতিমধ্যেই একটি ব্যাচ ডাউনলোড শুরু করেছেন। এটি শেষ না হওয়া পর্যন্ত অপেক্ষা করুন!")
    async with Drone.conversation(event.chat_id) as conv: 
        if s != True:
            await conv.send_message("আপনি যে মেসেজ থেকে ব্যাচ ডাউনলোড করতে চাচ্ছেন সেটির লিংক আমাকে এই মেসেজের রিপ্লাই হিসেবে দিন।", buttons=Button.force_reply())
            try:
                link = await conv.get_reply()
                try:
                    _link = get_link(link.text)
                except Exception:
                    await conv.send_message("কোনো লিংক পাওয়া যায় নি!")
            except Exception as e:
                print(e)
                return await conv.send_message("আপনার রেসপন্সের জন্য আর বেশি অপেক্ষা করতে পারছি না!")
            await conv.send_message("মাত্রই আমাকে যে লিংক দিলেন, ওইটা থেকে শুরু করে আপনি কতটি কনটেন্ট ডাউনলোড করতে চান তা এই মেসেজের রিপ্লাই হিসেবে আমাকে ইংরেজিতে লিখুন !", buttons=Button.force_reply())
            try:
                _range = await conv.get_reply()
            except Exception as e:
                print(e)
                return await conv.send_message("আপনার রেসপন্সের জন্য আর বেশি অপেক্ষা করতে পারছি না!")
            try:
                value = int(_range.text)
                if value > 100:
                    return await conv.send_message("প্রতিবার ব্যাচ ডাউনলোডে আপনি সর্বোচ্চ ৮০ টি ফাইল ডাউনলোড করতে পারবেন।")
            except ValueError:
                return await conv.send_message("রেঞ্জটি অবশ্যই বাস্তব ধনাত্মক সংখ্যা হতে হবে!")
            s, r = await check(userbot, Bot, _link)
            if s != True:
                await conv.send_message(r)
                return
            batch.append(f'{event.sender_id}')
            await run_batch(userbot, Bot, event.sender_id, _link, value) 
            conv.cancel()
            batch.pop(0)
            
            
async def run_batch(userbot, client, sender, link, _range):
    for i in range(_range):
        timer = 60
        if i < 25:
            timer = 15
        if i < 50 and i > 25:
            timer = 25
        if i < 200 and i > 50:
            timer = 40
        if not 't.me/c/' in link:
            if i < 25:
                timer = 2
            else:
                timer = 3
        try:
            await get_bulk_msg(userbot, client, sender, link, i) 
        except FloodWait as fw:
            await asyncio.sleep(fw.seconds + 8)
            await get_bulk_msg(userbot, client, sender, link, i)
        protection = await client.send_message(sender, f"আপনার অ্যাকাউন্টের নিরাপত্তা ও স্প্যাম হিসেবে শনাক্ত না হবার জন্য `{timer}` সেকেন্ড কার্যক্রম বন্ধ রাখা হচ্ছে!")
        time.sleep(timer)
        await protection.delete()
            
                

