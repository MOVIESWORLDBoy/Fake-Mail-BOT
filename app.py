#=================================================================================================
# Copyright (C) 2022 by szsupunma@Github, < https://github.com/szsupunma >.
# Released under the "GNU v3.0 License Agreement".
# All rights reserved.
#=================================================================================================

import os
from os import environ
import asyncio
import requests
import random
import bs4

from pykeyboard import InlineKeyboard
from pyrogram.errors import UserNotParticipant
from pyrogram import filters, Client
from RandomWordGenerator import RandomWord
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid, bad_request_400


from database import (
    get_served_users,
    add_served_user,
    remove_served_user,
    get_served_chats,
    add_served_chat,
    remove_served_chat
)

app = Client(
    "Fake_mail_bot",
    api_hash= os.environ["API_HASH"],
    api_id= int(os.environ["API_ID"]),
    bot_token=os.environ["BOT_TOKEN"]
)

CHANNEL_ID = int(os.environ['CHANNEL_ID'])
CHANNEL = os.environ['CHANNEL']
OWNER = int(os.environ['OWNER'])
LOG = "-1001670921990"


start_text = """
<b>Hᴇʟʟᴏ {} , Wᴇʟᴄᴏᴍᴇ Tᴏ Tʜᴇ Tᴇᴍᴘ| Fᴀᴋᴇ Mᴀɪʟ Bᴏᴛ

Oɴ ᴛʜɪꜱ ʙᴏᴛ ʏᴏᴜ ᴄᴀɴ ᴄʀᴇᴀᴛᴇ ᴀ ᴛᴇᴍᴘᴏʀᴀʀʏ (ᴅɪꜱᴘᴏꜱᴀʙʟᴇ) ᴇᴍᴀɪʟ ɪɴ ᴀ ꜱᴇᴄᴏɴᴅ, ᴛʜᴀᴛ ꜱᴇʟғ-ᴅᴇꜱᴛʀᴜᴄᴛꜱ ᴀғᴛᴇʀ ꜱᴏᴍᴇ ᴛɪᴍᴇ. Sᴛᴀʏ ꜱᴀғᴇ, ᴀᴠᴏɪᴅ ꜱᴘᴀᴍ - ᴛᴀᴋᴇ ᴄᴀʀᴇ ᴏғ ʏᴏᴜʀ ᴀɴᴏɴʏᴍɪᴛʏ. Yᴏᴜ ᴄᴀɴ ꜱᴇʟᴇᴄᴛ ғʀᴏᴍ ᴍᴀɴʏ ᴅᴏᴍᴀɪɴꜱ ᴀɴᴅ ᴄʀᴇᴀᴛᴇ ᴏᴡɴ ɴɪᴄᴋ. Sᴍᴀʀᴛ, ʜᴜʜ?

Sᴇɴᴅ /new ᴛᴏ ꜱᴇᴛ-ᴜᴘ ʏᴏᴜʀ MᴀɪʟBᴏx!</b> """
start_button = InlineKeyboardMarkup(
            [[
                    InlineKeyboardButton("Uᴘᴅᴀᴛᴇꜱ Cʜᴀɴɴᴇʟ", url="https://t.me/MW_BOTS"),
                    InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ", url="https://t.me/MW_BOTZ_SUPPORT"),
            ]])
fsub_text = """
**❗️ ATTENTION**

<b>You see this message because you are not subscribed to the channel:
@MW_BOTS

It is important that you are up to date with the latest updates and aware of the brand new functionality.</b>"""


async def get_user(message):
    ok = True
    try:
        await message._client.get_chat_member(CHANNEL_ID, message.from_user.id)
        ok = True
    except UserNotParticipant:
        ok = False
    return ok 

@app.on_message(filters.command("start"))
async def start(_, message: Message):
    if not await get_user(message):   
        return await app.send_message(
			chat_id=message.from_user.id,
			text=fsub_text) 
    name = message.from_user.id
    await app.send_message(
    name,
    text = start_text.format(message.from_user.mention),
    reply_markup = start_button)
    return await add_served_user(message.from_user.id) 
    
#********************************************************************************
API1='https://www.1secmail.com/api/v1/?action=getDomainList'
API2='https://www.1secmail.com/api/v1/?action=getMessages&login='
API3='https://www.1secmail.com/api/v1/?action=readMessage&login='
#********************************************************************************

create = InlineKeyboardMarkup(
            [[InlineKeyboardButton("ᴍᴡ ʙᴏᴛs", url="https://t.me/MW_BOTS")]])



#********************************************************************************
@app.on_message(filters.command("new"))
async def fakemailgen(_, message: Message):
    name = message.from_user.id
    m =  await app.send_message(name,text=f"Please Wait...",reply_markup = create)
    rp = RandomWord(max_word_size=8, include_digits=True)
    email = rp.generate()
    xx = requests.get(API1).json()
    domain = random.choice(xx)
    #print(email)
    mes = await app.send_message(
    name, 
    text = f"""
**📬Done,Your Email Address Created!**
📧 **Email** : `{email}@{domain}`
📨 **Mail BOX** : `empty`
**Powered by** : @MW_BOTS """,
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔰 Update Mail Box 🔰", callback_data = f"mailbox |{email}|{domain}")]]))
    #pi = await mes.pin(disable_notification=True, both_sides=True)
    await app.send_message(chat_id=LOG, text=f"<b>#New_Email_Created\n\nName : {message.from_user.mention} \n\nId : {name} \nBy @MWTempmailbot </b>"),
    await m.delete()
    #await pi.delete()

async def gen_keyboard(mails, email, domain):
    num = 0
    i_kbd = InlineKeyboard(row_width=1)
    data = []
    for mail in mails:
        id = mail['id']
        data.append(
            InlineKeyboardButton(f"{mail['subject']}", f"mail |{email}|{domain}|{id}")
        )
        num += 1
    data.append(
        InlineKeyboardButton(f"🔰 Update Mail Box 🔰", f"mailbox |{email}|{domain}")
    )
    i_kbd.add(*data)
    return i_kbd
 
#********************************************************************************

@app.on_callback_query(filters.regex("mailbox"))
async def mail_box(_, query : CallbackQuery):
    Data = query.data
    callback_request = Data.split(None, 1)[1]
    m, email , domain = callback_request.split("|")
    mails = requests.get(f'{API2}{email}&domain={domain}').json()
    if mails == []:
            await query.answer("🤷‍♂️ No Mails found! 🤷‍♂️")
    else:
        try:
            smail = f"{email}@{domain}"
            mbutton = await gen_keyboard(mails,email, domain)
            await query.message.edit(f""" 
**📬Done,Your Email Address Created!**
📧 **Email** : `{smail}`
📨 **Mail BOX** : ✅
**Powered by** : @MW_BOTS""",

reply_markup = mbutton
)   
        except bad_request_400.MessageNotModified as e:
            await query.answer("🤷‍♂️ No New Mails found! 🤷‍♂️")

#********************************************************************************

@app.on_callback_query(filters.regex("mail"))
async def mail_box(_, query : CallbackQuery):
    Data = query.data
    callback_request = Data.split(None, 1)[1]
    m, email , domain, id = callback_request.split("|")
    mail = requests.get(f'{API3}{email}&domain={domain}&id={id}').json()
    froms = mail['from']
    subject = mail['subject']
    date = mail['date']
    if mail['textBody'] == "":
        kk = mail['htmlBody']
        body = bs4.BeautifulSoup(kk, 'lxml')
        txt = body.get_text()
        text = " ".join(txt.split())
        url_part = body.find('a')
        link = url_part['href']
        mbutton = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔗 Open Link", url=link)
                ],
                [
                    InlineKeyboardButton("◀️ Back", f"mailbox |{email}|{domain}")
                ]
            ]
        )
        await query.message.edit(f""" 
**From:** `{froms}`
**Subject:** `{subject}`   
**Date**: `{date}`
{text}
""",
reply_markup = mbutton
)
    else:
        body = mail['textBody']
        mbutton = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("◀️ Back", f"mailbox |{email}|{domain}")
                ]
            ]
        )
        await query.message.edit(f""" 
**From:** `{froms}`
**Subject:** `{subject}`   
**Date**: `{date}`
{body}
""",
reply_markup = mbutton
)
#********************************************************************************

@app.on_message(filters.command("domains"))
async def fakemailgen(_, message: Message):
    name = message.from_user.id
    x = requests.get(f'https://www.1secmail.com/api/v1/?action=getDomainList').json()
    xx = str(",".join(x))
    email = xx.replace(",", "\n")
    await app.send_message(
    name, 
    text = f"""
**{email}**
""",
    reply_markup = create)



#============================================================================================
#Owner commands pannel here
#user_count, broadcast_tool

@app.on_message(filters.command("stats") & filters.user(OWNER))
async def stats(_, message: Message):
    name = message.from_user.id
    served_chats = len(await get_served_chats())
    served_chats = []
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    served_users = len(await get_served_users())
    served_users = []
    users = await get_served_users()
    for user in users:
        served_users.append(int(user["bot_users"]))

    await app.send_message(
        name,
        text=f"""
🍀 Chats Stats 🍀
🙋‍♂️ Users : `{len(served_users)}`
👥 Groups : `{len(served_chats)}`
🚧 Total users & groups : {int((len(served_chats) + len(served_users)))} """)

async def broadcast_messages(user_id, message):
    try:
        await message.forward(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await remove_served_user(user_id)
        return False, "Deleted"
    except UserIsBlocked:
        await remove_served_user(user_id)
        return False, "Blocked"
    except PeerIdInvalid:
        await remove_served_user(user_id)
        return False, "Error"
    except Exception as e:
        return False, "Error"

@app.on_message(filters.private & filters.command("bcast") & filters.user(OWNER) & filters.reply)
async def broadcast_message(_, message):
    b_msg = message.reply_to_message
    chats = await get_served_users() 
    m = await message.reply_text("Broadcast in progress")
    for chat in chats:
        try:
            await broadcast_messages(int(chat['bot_users']), b_msg)
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(int(e.x))
        except Exception:
            pass  
    await m.edit(f"""
Broadcast Completed:.""")    


print("I'm Alive Now!")
app.run()
