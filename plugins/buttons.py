from pyrogram import Client, types
import os

async def progress(name:str, message:types.Message, current:int, total:int):
    await message.edit_text(F"Uploading: / {name} \ {current * 100 / total:.1f}%")

@Client.on_callback_query()
async def buttons(client:Client, callback_query:types.CallbackQuery):
    if callback_query.data == "delete":
        return await callback_query.message.delete()
    elif callback_query.data == "kill":
        download = client.downloads.get(str(callback_query.from_user.id))
        if download:
            data = download.get("data")
            download["kill"] = True
            return await callback_query.answer(F"Killed the download of\n{data['artist']['name']} - {data['title']}...")
        else:
            return await callback_query.answer("Nothing is getting downloaded...")
    data = callback_query.data.split("|")
    relate = data[0]
    id = data[1]
    if relate == "goartist":
        artist = client.dezapi.get_artist(id)
        keyboard = [
            [
                types.InlineKeyboardButton(text="Tracks 💿", switch_inline_query_current_chat=F".trks {artist['id']}"),
                types.InlineKeyboardButton(text="Albums 📼", switch_inline_query_current_chat=F".albs {artist['id']}")
            ],
            [types.InlineKeyboardButton(text="Delete 💣", callback_data="delete")]
        ]
        markup = types.InlineKeyboardMarkup(keyboard)
        await callback_query.message.reply_photo(photo=artist['picture_big'], caption=artist['name'], reply_markup=markup)
        await callback_query.answer(F"Went to {artist['name']}'s Info...")
    elif relate == "goalbum":
        album = client.dezapi.get_album(id)
        tracks = album['tracks']['data']
        keyboard = []
        counter = 1
        for track in tracks:
            key = [types.InlineKeyboardButton(F"{counter}. {track['title']} 💿", callback_data=F"download|{track['id']}")]
            keyboard.append(key)
            counter += 1
        keyboard.append([types.InlineKeyboardButton(F"Get all Tracks 💽", callback_data=F"getall|{album['id']}")])
        keyboard.append([types.InlineKeyboardButton(F"Go to Artist 👤", callback_data=F"goartist|{album['artist']['id']}")])
        keyboard.append([types.InlineKeyboardButton(text="Delete 💣", callback_data="delete")])
        markup = types.InlineKeyboardMarkup(keyboard)
        await callback_query.message.reply_photo(photo=album['cover_big'], caption=F"{album['title']} - {album['artist']['name']}", reply_markup=markup)
        await callback_query.answer(F"Went to {album['artist']['name']}'s {album['title']} Album...")
    elif relate == "getall":
        downloading = client.downloads.get(str(callback_query.from_user.id))
        if downloading:
            await callback_query.answer("You have to wait...")
            await callback_query.message.reply_text(text=F"You are currently downloading:\n{downloading['data']['artist']['name']} - {downloading['data']['title']}\nPlease wait for it to complete!")
        else:
            album = client.dezapi.get_album(id)
            tracks = album['tracks']['data']
            client.downloads[str(callback_query.from_user.id)] = {"data": album, "kill": False}
            await callback_query.answer(F"Downloading {album['title']} album...")
            queue = await callback_query.message.reply_text(text=F"Uploading...")
            counter = 1
            for track in tracks:
                if client.downloads.get(str(callback_query.from_user.id)).get("kill") == True:
                    break
                download = client.dezlog.download_trackdee(
                    track['link'],
                    output_dir=F"./musics/",
                    quality_download="FLAC",
                    recursive_quality=True,
                    recursive_download=True,
                    method_save=1
                )
                await client.send_audio(chat_id=callback_query.message.chat.id, audio=download.song_path, title=track['title'], performer=track['artist']['name'], duration=track['duration'], progress=await progress(track['title'], queue, counter, len(tracks)))
                os.remove(download.song_path)
                counter += 1
            await queue.delete()
            await callback_query.message.reply_text(text="Done!")
            del client.downloads[str(callback_query.from_user.id)]
    elif relate == "download":
        track = client.dezapi.get_track(id)
        await callback_query.answer(F"Downloading {track['title']} track...")
        download = client.dezlog.download_trackdee(
            track['link'],
            output_dir=F"./musics/",
            quality_download="FLAC",
            recursive_quality=True,
            recursive_download=True,
            method_save=1
        )
        await client.send_audio(chat_id=callback_query.message.chat.id, audio=download.song_path, title=track['title'], performer=track['artist']['name'], duration=track['duration'])
        os.remove(download.song_path)
