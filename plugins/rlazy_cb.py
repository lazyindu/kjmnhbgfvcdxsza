from database.lazy_utils import progress_for_pyrogram, convert, humanbytes
from pyrogram import Client, filters, enums
from pyrogram.types import ForceReply , CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from database.users_chats_db import db
from database.lazy_set import escape_invalid_curly_brackets
from database.lazy_ffmpeg import take_screen_shot, fix_thumb
from datetime import timedelta
from Script import script
import os 
import random
import humanize
from PIL import Image
import time

@Client.on_callback_query(filters.regex('rename'))
async def rename(bot,update):
	user_id = update.message.chat.id
	date = update.message.date
	await update.message.delete()
	await update.message.reply_text("»»——— 𝙋𝙡𝙚𝙖𝙨𝙚 𝙚𝙣𝙩𝙚𝙧 𝙣𝙚𝙬 𝙛𝙞𝙡𝙚 𝙣𝙖𝙢𝙚...",	
	reply_to_message_id=update.message.reply_to_message.id,  
	reply_markup=ForceReply(True))  

@Client.on_callback_query(filters.regex("upload"))
async def doc(bot, update):
    type = update.data.split("_")[1]
    new_name = update.message.text
    new_filename = new_name.split(":-")[1]
    file = update.message.reply_to_message
    file_path = f"downloads/{new_filename}"
    ms = await update.message.edit("\n༻☬ད 𝘽𝙪𝙞𝙡𝙙𝙞𝙣𝙜 𝙇𝙖𝙯𝙮 𝙈𝙚𝙩𝙖𝘿𝙖𝙩𝙖...")
    c_time = time.time()
    try:
        path = await bot.download_media(
                message=file,
                progress=progress_for_pyrogram,
                progress_args=("**\n  ღ♡ ꜰɪʟᴇ ᴜɴᴅᴇʀ ᴄᴏɴꜱᴛʀᴜᴄᴛɪᴏɴ... ♡♪**", ms, c_time))
    except Exception as e:
        await ms.edit(e)
        return 
    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name =f"downloads/{dow_file_name}"
    os.rename(old_file_name, file_path)
    duration = 0
    try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
           duration = metadata.get('duration').seconds
    except:
        pass
    user_id = int(update.message.chat.id) 
    ph_path = None 
    media = getattr(file, file.media.value)
    filesize = humanize.naturalsize(media.file_size) 
    c_caption = await db.get_caption(update.message.chat.id)
    c_thumb = await db.get_thumbnail(update.message.chat.id)
    if c_caption:
         try:
             caption = c_caption.format(filename=new_filename, filesize=humanize.naturalsize(media.file_size), duration=convert(duration))
         except Exception as e:
             await ms.edit(text=f"Your caption Error unexpected keyword ●> ({e})")
             return 
    else:
        caption = f"**{new_filename}** \n\n⚡️Data costs: `{filesize}`"
    if (media.thumbs or c_thumb):
        if c_thumb:
           ph_path = await bot.download_media(c_thumb) 
        else:
           ph_path = await bot.download_media(media.thumbs[0].file_id)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")
    await ms.edit("三 𝘗𝘳𝘦𝘱𝘢𝘳𝘪𝘯𝘨 𝘵𝘰 𝘳𝘦𝘤𝘦𝘪𝘷𝘦 𝘓𝘢𝘻𝘺 𝘧𝘪𝘭𝘦...︻デ═一")
    c_time = time.time() 
    try:
       if type == "document":
          await bot.send_document(
	        update.message.chat.id,
                   document=file_path,
                   thumb=ph_path, 
                   caption=caption, 
                   progress=progress_for_pyrogram,
                   progress_args=( "**⎝⎝✧ ʀᴇᴄɪᴇᴠɪɴɢ ꜰɪʟᴇ ꜰʀᴏᴍ ʟᴀᴢʏ ꜱᴇʀᴠᴇʀ ✧⎠⎠**",  ms, c_time))
       elif type == "video": 
           await bot.send_video(
	        update.message.chat.id,
	        video=file_path,
	        caption=caption,
	        thumb=ph_path,
	        duration=duration,
	        progress=progress_for_pyrogram,
	        progress_args=( "**⎝⎝✧ ʀᴇᴄɪᴇᴠɪɴɢ ꜰɪʟᴇ ꜰʀᴏᴍ ʟᴀᴢʏ ꜱᴇʀᴠᴇʀ ✧⎠⎠**",  ms, c_time))
       elif type == "audio": 
           await bot.send_audio(
	        update.message.chat.id,
	        audio=file_path,
	        caption=caption,
	        thumb=ph_path,
	        duration=duration,
	        progress=progress_for_pyrogram,
	        progress_args=( "**⎝⎝✧ ʀᴇᴄɪᴇᴠɪɴɢ ꜰɪʟᴇ ꜰʀᴏᴍ ʟᴀᴢʏ ꜱᴇʀᴠᴇʀ ✧⎠⎠**",  ms, c_time   )) 
    except Exception as e: 
        await ms.edit(f" Erro {e}") 
        os.remove(file_path)
        if ph_path:
          os.remove(ph_path)
        return 
    await ms.delete() 
    os.remove(file_path) 
    if ph_path:
       os.remove(ph_path) 


@Client.on_callback_query()
async def lz_cb_handler(client: Client, query: CallbackQuery):
    if query.data == "getlazythumbnail":
        buttons = [
            [
            InlineKeyboardButton("D͢o͢n͢a͢t͢e͢ L͢a͢z͢y͢D͢e͢v͢", callback_data="thdonatelazydev"),
            ],
            [ InlineKeyboardButton("<- G̳O̳ ̳B̳A̳C̳K̳  ⨳", callback_data="lazyhome") ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.LZTHMB_TEXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "thdonatelazydev":
        buttons = [
            [ InlineKeyboardButton("<- G̳O̳ ̳B̳A̳C̳K̳  ⨳", callback_data="getlazythumbnail") ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.DNT_TEXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "getlazylink":
        buttons = [
            [
            InlineKeyboardButton("D͢o͢n͢a͢t͢e͢ L͢a͢z͢y͢D͢e͢v͢", callback_data="linkdonatelazydev"),
            ],
            [ InlineKeyboardButton("<- G̳O̳ ̳B̳A̳C̳K̳  ⨳", callback_data="lazyhome") ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.LZLINK_TEXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "linkdonatelazydev":
        buttons = [
            [ InlineKeyboardButton("<- G̳O̳ ̳B̳A̳C̳K̳  ⨳", callback_data="getlazylink") ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.DNT_TEXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "lazyhome":
        text = f"""\n⨳ *•.¸♡ L҉ΛＺ𝐲 ＭⓄｄ𝓔 ♡¸.•* ⨳\n\n**Please tell, what should i do with this file.?**\n"""
        buttons = [[ InlineKeyboardButton("📝✧✧ S𝚝ar𝚝 re𝚗aᗰi𝚗g ✧✧📝", callback_data="rename") ],
                           [ InlineKeyboardButton("📸G͢e͢t͢ T͢h͢u͢m͢b͢n͢a͢i͢l͢ ᶜᵒᵐⁱⁿᵍ ˢᵒᵒⁿ", callback_data="getlazythumbnail") ],
                           [ InlineKeyboardButton("🔏G͢e͢n͢e͢r͢a͢t͢e͢ L͢i͢n͢k͢ ᶜᵒᵐⁱⁿᵍ ˢᵒᵒⁿ", callback_data="getlazylink") ],
                           [ InlineKeyboardButton("⨳  C L Ф S Ξ  ⨳", callback_data="cancel") ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
                    text=text,
                    reply_markup=reply_markup,
                    parse_mode=enums.ParseMode.HTML
                )    
    elif query.data == "requireauth":
        buttons = [
            [ InlineKeyboardButton("⨳  C L Ф S Ξ  ⨳", callback_data="cancel") ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.REQ_AUTH_TEXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "reqauthgetlazythumbnail":
        buttons = [
            [
            InlineKeyboardButton("D͢o͢n͢a͢t͢e͢ L͢a͢z͢y͢D͢e͢v͢", callback_data="thdonatelazydev"),
            ],
            [ InlineKeyboardButton("<- G̳O̳ ̳B̳A̳C̳K̳  ⨳", callback_data="reqauthlazyhome") ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.LZTHMB_TEXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "reqauthlazyhome":
        text = f"""\n⨳ *•.¸♡ L҉ΛＺ𝐲 ＭⓄｄ𝓔 ♡¸.•* ⨳\n\n**Please tell, what should i do with this file.?**\n"""
        buttons = [[ InlineKeyboardButton("📝✧✧ S𝚝ar𝚝 re𝚗aᗰi𝚗g ✧✧📝", callback_data="requireauth") ],
                           [ InlineKeyboardButton("📸G͢e͢t͢ T͢h͢u͢m͢b͢n͢a͢i͢l͢ ᶜᵒᵐⁱⁿᵍ ˢᵒᵒⁿ", callback_data="reqauthgetlazythumbnail") ],
                           [ InlineKeyboardButton("🔏G͢e͢n͢e͢r͢a͢t͢e͢ L͢i͢n͢k͢ ᶜᵒᵐⁱⁿᵍ ˢᵒᵒⁿ", callback_data="reqauthgetlazylink") ],
                           [ InlineKeyboardButton("⨳  C L Ф S Ξ  ⨳", callback_data="cancel") ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
                    text=text,
                    reply_markup=reply_markup,
                    parse_mode=enums.ParseMode.HTML
                )
    elif query.data == "reqauthgetlazylink":
        buttons = [
            [
            InlineKeyboardButton("D͢o͢n͢a͢t͢e͢ L͢a͢z͢y͢D͢e͢v͢", callback_data="linkdonatelazydev"),
            ],
            [ InlineKeyboardButton("<- G̳O̳ ̳B̳A̳C̳K̳  ⨳", callback_data="reqauthlazyhome") ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.LZLINK_TEXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "cancel":
        try:
            await query.message.delete()
        except:
            return