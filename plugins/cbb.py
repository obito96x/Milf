#Coded by @Its_Tartaglia_Childe

from pyrogram import Client 
from bot import Bot
from config import OWNER_ID, ABOUT_TXT, HELP_TXT, START_MSG
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "help":
        await query.message.edit_text(
            text = HELP_TXT.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('ʜᴏᴍᴇ​', callback_data='start'),
                        InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data='close')
                    ]
                ]
            )
        )
    elif data == "about":
        await query.message.edit_text(
            text = ABOUT_TXT.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
                     InlineKeyboardButton('ᴄʟᴏꜱᴇ', callback_data='close')]
                ]
            )
        )
    elif data == "start":
        await query.message.edit_text(
            text = START_MSG.format(query.from_user.mention),
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("ʜᴇʟᴘ", callback_data='help'),
             InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data='about')],
            [InlineKeyboardButton('ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ', url='https://t.me/Anime_X_Hunters'),
             InlineKeyboardButton('ᴏɴɢᴏɪɴɢ ᴄʜᴀɴɴᴇʟ', url='https://t.me/Ongoing_Anime_X_Hunter')],
             [InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data='close')]
        ])
        )
    
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
