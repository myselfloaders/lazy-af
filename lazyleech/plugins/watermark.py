import os
import tempfile
from pyrogram import Client, filters
from .. import ALL_CHATS, help_dict
from ..utils.misc import get_file_mimetype, watermark_photo

@Client.on_message(filters.command(['setwatermark', 'setwatermark@Miku_Nakano_Leeching_Bot']) & filters.chat(ALL_CHATS))
async def savewatermark(client, message):
    reply = message.reply_to_message
    document = message.document
    photo = message.photo
    thumbset = False
    user_id = message.from_user.id
    watermark_path = os.path.join(str(user_id), 'watermark.jpg')
    os.makedirs(str(user_id), exist_ok=True)
    if document or photo:
        if photo or (document.file_size < 10485760 and os.path.splitext(document.file_name)[1] and (not document.mime_type or document.mime_type.startswith('image/'))):
            with tempfile.NamedTemporaryFile(dir=str(user_id)) as tempthumb:
                await message.download(tempthumb.name)
                mimetype = await get_file_mimetype(tempthumb.name)
                if mimetype.startswith('image/'):
                    thumbset = True
                    with open(watermark_path, 'wb') as watermark_file:
                        while True:
                            chunk = tempthumb.read(10)
                            if not chunk:
                                break
                            watermark_file.write(chunk)
    if not getattr(reply, 'empty', True) and not thumbset:
        document = reply.document
        photo = reply.photo
        if document or photo:
            if photo or (document.file_size < 10485760 and os.path.splitext(document.file_name)[1] and (not document.mime_type or document.mime_type.startswith('image/'))):
                with tempfile.NamedTemporaryFile(dir=str(user_id)) as tempthumb:
                    await reply.download(tempthumb.name)
                    mimetype = await get_file_mimetype(tempthumb.name)
                    if mimetype.startswith('image/'):
                        thumbset = True
                        with open(watermark_path, 'wb') as watermark_file:
                            while True:
                                chunk = tempthumb.read(10)
                                if not chunk:
                                    break
                                watermark_file.write(chunk)
    if thumbset:
        thumbnail = os.path.join(str(user_id), 'thumbnail.jpg')
        watermarked_thumbnail = os.path.join(str(user_id), 'watermarked_thumbnail.jpg')
        if os.path.isfile(thumbnail):
            await watermark_photo(thumbnail, watermark_path, watermarked_thumbnail)
        await message.reply_text('All Done! Onii-chan')
    else:
        await message.reply_text('I tried, But I am unable to find any watermark Onii-chan')

@Client.on_message(filters.command(['delwatermark', 'delwatermark@Miku_Nakano_Leeching_Bot']) & filters.chat(ALL_CHATS))
async def rmwatermark(client, message):
    for path in ('watermark', 'watermarked_thumbnail'):
        path = os.path.join(str(message.from_user.id), f'{path}.jpg')
        if os.path.isfile(path):
            os.remove(path)
    await message.reply_text('I have thrown the old watermark away, Now we can proceed further  Onii-chan')

@Client.on_message(filters.command('testwatermark', 'testwatermark@Miku_Nakano_Leeching_Bot') & filters.chat(ALL_CHATS))
async def testwatermark(client, message):
    watermark = os.path.join(str(message.from_user.id), 'watermark.jpg')
    if not os.path.isfile(watermark):
        await message.reply_text('I tried, But I am unable to find any watermark Onii-chan')
        return
    watermarked_thumbnail = os.path.join(str(message.from_user.id), 'watermarked_thumbnail.jpg')
    with tempfile.NamedTemporaryFile(suffix='.jpg') as file:
        to_upload = watermarked_thumbnail
        if not os.path.isfile(to_upload):
            await watermark_photo('testwatermark.jpg', watermark, file.name)
            to_upload = file.name
        await message.reply_photo(to_upload)

help_dict['watermark'] = ('Watermark',
'''/setwatermark <i>&lt;as reply to image or as a caption&gt;</i>
/delwatermark <b>I'll throw away useless stuff away from you Onii-chan
/testwatermark''')
