import os

import tempfile

from pyrogram import Client, filters

from .. import ALL_CHATS, help_dict

from ..utils.misc import convert_to_jpg, get_file_mimetype, watermark_photo

@Client.on_message(filters.command(['thumbnail', 'thumbnail@Leech_VLbot']) & filters.chat(ALL_CHATS))

async def savethumbnail(client, message):

    reply = message.reply_to_message

    document = message.document

    photo = message.photo

    thumbset = False

    user_id = message.from_user.id

    thumbnail_path = os.path.join(str(user_id), 'thumbnail.jpg')

    os.makedirs(str(user_id), exist_ok=True)

    if document or photo:

        if photo or (document.file_size < 10485760 and os.path.splitext(document.file_name)[1] and (not document.mime_type or document.mime_type.startswith('image/'))):

            with tempfile.NamedTemporaryFile(dir=str(user_id)) as tempthumb:

                await message.download(tempthumb.name)

                mimetype = await get_file_mimetype(tempthumb.name)

                if mimetype.startswith('image/'):

                    await convert_to_jpg(tempthumb.name, thumbnail_path)

                    thumbset = True

    if not getattr(reply, 'empty', True) and not thumbset:

        document = reply.document

        photo = reply.photo

        if document or photo:

            if photo or (document.file_size < 10485760 and os.path.splitext(document.file_name)[1] and (not document.mime_type or document.mime_type.startswith('image/'))):

                with tempfile.NamedTemporaryFile(dir=str(user_id)) as tempthumb:

                    await reply.download(tempthumb.name)

                    mimetype = await get_file_mimetype(tempthumb.name)

                    if mimetype.startswith('image/'):

                        await convert_to_jpg(tempthumb.name, thumbnail_path)

                        thumbset = True

    if thumbset:

        watermark = os.path.join(str(user_id), 'watermark.jpg')

        watermarked_thumbnail = os.path.join(str(user_id), 'watermarked_thumbnail.jpg')

        if os.path.isfile(watermark):

            await watermark_photo(thumbnail_path, watermark, watermarked_thumbnail)

        await message.reply_text('Thumbnail Added Successfully!')

    else:

        await message.reply_text('Give Me A Pic First ????????')

@Client.on_message(filters.command(['delthumbnail', 'deletethumbnail@Leech_VLbot']) & filters.chat(ALL_CHATS))

async def rmthumbnail(client, message):

    for path in ('thumbnail', 'watermarked_thumbnail'):

        path = os.path.join(str(message.from_user.id), f'{path}.jpg')

        if os.path.isfile(path):

            os.remove(path)

    await message.reply_text('Thumbnail Deleted Successfully!')

help_dict['thumbnail'] = ('Thumbnail',

'''/setthumbnail <b>Set Custom Thumbnail</b>

/delthumbnail <b>Delete Existing Thumbnail</b>''')
