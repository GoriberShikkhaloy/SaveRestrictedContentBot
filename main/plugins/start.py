#Github.com/Vasusen-code

import os
from .. import bot as Drone
from telethon import events, Button

from ethon.mystarts import start_srb
    
S = '/' + 's' + 't' + 'a' + 'r' + 't'

@Drone.on(events.callbackquery.CallbackQuery(data="set"))
async def sett(event):    
    Drone = event.client                    
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    async with Drone.conversation(event.chat_id) as conv: 
        xx = await conv.send_message("এই মেসেজের রিপ্লাই হিসেবে কোনো একটা ছবি দিন, যেটা আপনি থাম্বনেইল হিসেবে ব্যবহার করতে চান।")
        x = await conv.get_reply()
        if not x.media:
            xx.edit("কোনো মিডিয়া পাওয়া যায় নি।")
        mime = x.file.mime_type
        if not 'png' in mime:
            if not 'jpg' in mime:
                if not 'jpeg' in mime:
                    return await xx.edit("কোনো ছবি পাওয়া যায় নি।")
        await xx.delete()
        t = await event.client.send_message(event.chat_id, 'চেষ্টা করা হচ্ছে...')
        path = await event.client.download_media(x.media)
        if os.path.exists(f'{event.sender_id}.jpg'):
            os.remove(f'{event.sender_id}.jpg')
        os.rename(path, f'./{event.sender_id}.jpg')
        await t.edit("অস্থায়ী থাম্বনেইল সেট করা হয়েছে!")
        
@Drone.on(events.callbackquery.CallbackQuery(data="rem"))
async def remt(event):  
    Drone = event.client            
    await event.edit(' চেষ্টা করা হচ্ছে...')
    try:
        os.remove(f'{event.sender_id}.jpg')
        await event.edit('মুছে ফেলা হয়েছে!')
    except Exception:
        await event.edit("কোনো থাম্বনেইল নেই.")                        
  
@Drone.on(events.NewMessage(incoming=True, pattern=f"{S}"))
async def start(event):
    text = "যে মেসেজটি থেকে কোনো ফাইল ডাউনলোড করতে চান সেটির লিংক আমাকে দিন।\n\n**সত্ত্বাধিকারী:** দ্যা প্রফেসর ッ"
    await start_srb(event, text)
    
