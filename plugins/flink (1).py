from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, CallbackQuery
from bot import Bot

try:
    from .utils import Bot_config, Message_config # type: ignore

    ADMIN_USER = Bot_config.is_admin
    ENCODE_MSG = Message_config.encode
    GET_MESSAGE_ID = Message_config.get_message_id

except ImportError:
    try:
        from helper_func import is_admin as ADMIN_USER  # type: ignore 
    except ImportError:
        from config import ADMINS # type: ignore
        ADMIN_USER = filters.user(ADMINS)

    from helper_func import encode as ENCODE_MSG, get_message_id as GET_MESSAGE_ID # type: ignore 
    

EXAMPLES = """Exᴀᴍᴘʟᴇs: 
<blockquote expandable><code>360P = 2, 480P = 2, 720P = 2
1080P = 2, HDRIP = 1, 4K = 1</code>

<code>360P = 1, 480P = 1, 720P = 1
1080P = 1</code>
                                      
<code>360P = 1, 480P = 1, 720P = 1
1080P = 1, HDRIP = 1, 4K = 1</code>  

<code>480P = 2, 720P = 2, 1080P = 2 
HDRIP = 1, 4K = 1</code></blockquote>"""


closeButton = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data = 'close')]])
cancelKeyboard = ReplyKeyboardMarkup([['CANCEL']], one_time_keyboard=True, resize_keyboard=True)

format_data = {}


@Bot.on_message(filters.command('flink') & filters.private & ADMIN_USER)
async def handle_formated_link(client, message):
    user_id = message.from_user.id
    wait_msg = await message.reply("<b><i>ᴡᴀɪᴛ ᴀ sᴇᴄᴏɴᴅ..</i></b>", quote=True)

    await format_status_msg(wait_msg, user_id)


#===============================================================================================================================================================================================================
# -----------------------  HELPER FUNCTIONS FOR MANAGING FLINK QUERY PROCESS  --------------------------
#===============================================================================================================================================================================================================


async def start_flink_process(client: Bot, query: CallbackQuery):
    user_id = query.from_user.id

    link_formats = format_data.get(user_id)
    if not link_formats:
        return await query.answer('⚠️ Fɪʀsᴛ sᴇᴛ ᴛʜᴇ ʟɪɴᴋ ғᴏʀᴍᴀᴛ', show_alert=True)
        
    link = client.db_channel.invite_link
    channel = f"<a href={link}>ᴅʙ ᴄʜᴀɴɴᴇʟ</a>" if link else 'ᴅʙ ᴄʜᴀɴɴᴇʟ'

    while True:
        try:
            tmp = await query.message.reply(
                text=f"<b><blockquote>Fᴏʀᴡᴀʀᴅ ᴛʜᴇ Mᴇssᴀɢᴇ ғʀᴏᴍ {channel} (ᴡɪᴛʜ ǫᴜᴏᴛᴇs)..</blockquote>\n<blockquote>Oʀ Sᴇɴᴅ ᴛʜᴇ {channel} Pᴏsᴛ Lɪɴᴋ</blockquote></b>",
                reply_markup=cancelKeyboard,
                disable_web_page_preview=True
            )

            channel_message = await client.listen(chat_id=user_id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)))

            if channel_message.text == 'CANCEL':
                return await del_msg(channel_message, tmp)

        except:
            try: return await del_msg(tmp)
            except: return
            
        msg_id = await GET_MESSAGE_ID(client, channel_message)

        if msg_id:
            await del_msg(tmp)
            break
        else:
            await del_msg(tmp)
                
            await channel_message.reply(
                f"<b>❌ Eʀʀᴏʀ..\n<blockquote>Tʜɪs Fᴏʀᴡᴀʀᴅᴇᴅ ᴘᴏsᴛ ᴏʀ ᴍᴇssᴀɢᴇ ʟɪɴᴋ ɪs ɴᴏᴛ ғʀᴏᴍ ᴍʏ {channel}</blockquote></b>", 
                quote=True, 
                reply_markup=closeButton,
                disable_web_page_preview=True
            )
            continue

    format_lines = link_formats.splitlines()

    output_txt = []

    for line in format_lines:
        msg_txt_and_lengths = line.split(',')
        tmp_list = []

        for msg_data in msg_txt_and_lengths:
            msg_txt, start_with_msg_len = msg_data.strip().split(' = ')

            if ':' in start_with_msg_len:
                start, msg_len = start_with_msg_len.split(':')
                start, msg_len = int(start), int(msg_len)
            else:
                start = 0
                msg_len = int(start_with_msg_len)

            if msg_len == 1:
                msg_id += start 

                msg = f'get-{msg_id * abs(client.db_channel.id)}'
                msg_id += 1
                
            else:
                msg_id += start

                first_msg = f'{msg_id * abs(client.db_channel.id)}'
                msg_id += (msg_len-1)

                last_msg = f'{msg_id * abs(client.db_channel.id)}'
                msg_id += 1

                msg = f'get-{first_msg}-{last_msg}'
                
            encoded_msg = await ENCODE_MSG(msg)
            msg_link = f"https://t.me/{client.username}?start={encoded_msg}"

            tmp_list.append(f'{msg_txt} - {msg_link}')

        output_txt.append(" && ".join(tmp_list))

    final_message = '\n'.join(output_txt)
        
    inline_buttons = make_inline_button(final_message)
    await channel_message.reply(text=f'<b>⬇️ Bᴇʟᴏᴡ ɪs ᴛʜᴇ ғᴏʀᴍᴀᴛᴇᴅ ʟɪɴᴋ::</b>\n\n<blockquote><code>{final_message}</code></blockquote>', reply_markup=inline_buttons, quote=True, disable_web_page_preview=True)



async def change_flink_format(client: Bot, query: CallbackQuery):
    user_id = query.from_user.id
    
    temp = await query.message.reply(
        f'<b>Sᴇɴᴅ ʟɪɴᴋ ғᴏʀᴍᴀᴛ: Qᴜᴀʟɪᴛʏ ᴡɪᴛʜ ʀᴇsᴘᴇᴄᴛɪᴠᴇ ᴛᴏ ᴍᴇssᴀɢᴇ ʟᴇɴɢᴛʜ\n\n{EXAMPLES}</b>',
        reply_markup=cancelKeyboard
    )

    rcv_msg = await client.listen(chat_id=user_id)
    await del_msg(temp)

    TEXT = rcv_msg.text

    if TEXT is None:
        return await rcv_msg.reply("<b>⚠️ Pʟᴇᴀsᴇ, ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ɪɴᴘᴜᴛ (ᴛᴇxᴛ ᴍᴇssᴀɢᴇ ᴏɴʟʏ)</b>", reply_markup=closeButton, quote=True)

    if TEXT == 'CANCEL':
        return await rcv_msg.reply(f"<b><i>🆑 Oᴘᴇʀᴀᴛɪᴏɴ Cᴀɴᴄᴇʟʟᴇᴅ...</i></b>", reply_markup=closeButton, quote=True)
        
    format_lines = TEXT.splitlines()

    try:
        for line in format_lines:
            msg_txt_and_lengths = line.split(',')

            for msg_data in msg_txt_and_lengths:
                msg_txt, start_with_msg_len = msg_data.strip().split(' = ')
                    
                if ':' in start_with_msg_len:
                    start, msg_len = start_with_msg_len.split(':')
                    start, msg_len = int(start), int(msg_len)
                else:
                        #start = 0
                    msg_len = int(start_with_msg_len)

    except Exception as e:
        print(f"---- Invalide format received ----\nFormat: {TEXT}\n\nReason: {e}\n-----------------------")
        return await rcv_msg.reply(
            f"<b>⚠️ Iɴᴠᴀʟɪᴅ Fᴏʀᴍᴀᴛ, ғᴏʟʟᴏᴡ ʙᴇʟᴏᴡ\n\n{EXAMPLES}</b>", 
            reply_markup=closeButton,
            quote=True
        )
        
    else:
        format_data[user_id] = TEXT
        return await rcv_msg.reply(
            f"<b><i>Lɪɴᴋ Fᴏʀᴍᴀᴛ ᴀᴅᴅᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ ✅</i></b>", 
            reply_markup=closeButton,
            quote=True
        )


#===============================================================================================================================================================================================================
# --------------------------------------- OTHER HELPER FUNCTIONS --------------------------------------
#===============================================================================================================================================================================================================

async def del_msg(*msgs):
    for msg in msgs:
        try: await msg.delete()
        except: pass


def make_inline_button(text: str) -> ReplyKeyboardMarkup:
    inline_buttons = []
    button_lines = text.splitlines()

    for line in button_lines:
        tmp_buttons = []
        buttons_nums = line.split(' && ')

        for button in buttons_nums:
            try:
                button_txt,  button_link = button.split(' - ') 
            except Exception as e:
                print(f"! Exception in function (make_inline_button): {e}")
                return None
            
            tmp_buttons.append(InlineKeyboardButton(text=button_txt, url=button_link))

        inline_buttons.append(tmp_buttons)
    
    return InlineKeyboardMarkup(inline_buttons)


async def format_status_msg(message, user_id: int) -> str:
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('• sᴇᴛ ғᴏʀᴍᴀᴛ •', callback_data='flink:change_format')
            ],
            [
                InlineKeyboardButton('• sᴛᴀʀᴛ ᴘʀᴏᴄᴇss •', callback_data='flink:start')
            ],
            [
                InlineKeyboardButton('🔄', callback_data='flink:status'),
                InlineKeyboardButton("✖️", callback_data = 'close')
            ]
        ]
    )

    link_format = format_data.get(user_id, '--- Nᴏɴᴇ ---')

    await message.edit(
        text=f"<b>›› ғᴏʀᴍᴀᴛᴇᴅ ʟɪɴᴋ:\n\n›› ᴄᴜʀʀᴇɴᴛ ғᴏʀᴍᴀᴛ\n<blockquote><code>{link_format}</code></blockquote></b>",
        reply_markup=buttons
    )
