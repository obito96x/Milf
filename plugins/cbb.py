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
            text = HELP_TXT,
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('​🇸​​🇺​​🇵​​🇵​​🇴​​🇷​​🇹​ ​🇬​​🇷​​🇴​​🇺​​🇵​', url='https://t.me/Hunters_Discussion'),
                        InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data='close')
                    ]
                ]
            )
        )
    elif data == "about":
        await query.message.edit_text(
            text = ABOUT_TXT,
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
            text = START_MSG,
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
