import logging
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
from pyrogram.types import Message, InlineKeyboardButton
from pyrogram import Client, filters, enums
import datetime
import time
from database.users_chats_db import db
from info import ADMINS
import asyncio
        
@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
# vazha മരത്തെ കളിയാക്കിയവർ ###fi
async def verupikkals(bot, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='Broadcasting your messages...'
    )
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    for user in users:
        try:
            await b_msg.copy(user)
            done = done + 1
            await asyncio.sleep(2)
        except:
            failed = failed + 1
    await sts.edit(f"Broadcast Completed:\nTotal Users {total_users}\nSuccess: {done}\nfailed: {failed}")



@Client.on_message(filters.command("group_broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_group(bot, message):
    groups = await db.get_all_chats()
    b_msg = message.reply_to_message
    sts = await message.reply_text(text='Broadcasting your messages To Groups...')
    total_groups = await db.total_chat_count()
    done = 0
    failed = 0
    for group in groups:
        try:
            await b_msg.copy(group)
            done = done + 1
            await asyncio.sleep(2)
        except:
            failed = failed + 1
    await sts.edit(f"Broadcast Completed:\nTotal Chats {total_users}\nSuccess: {done}\nfailed: {failed}")

            
async def broadcast_messages_group(chat_id, message):
    try:
        await message.copy(chat_id=chat_id)
        return True, "Succes", 'mm'
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await broadcast_messages_group(chat_id, message)
    except Exception as e:
        await db.delete_chat(int(chat_id))
        logging.info(f"{chat_id} - PeerIdInvalid")
        return False, "deleted", f'{e}'
    


async def broadcast_messages(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id}-Removed from Database, since deleted account.")
        return False, "Deleted"
    except UserIsBlocked:
        logging.info(f"{user_id} -Blocked the bot.")
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id} - PeerIdInvalid")
        return False, "Error"
    except Exception as e:
        return False, "Error"
