import pyrogram, textwrap, os

@pyrogram.Client.on_callback_query()
async def buttons(client:pyrogram.Client, callback_query:pyrogram.types.CallbackQuery):
    if callback_query.data == "delete":
        return await callback_query.message.delete()
    data = callback_query.data.split("|")
    relate = data[0]
    id = data[1]
    if relate == "goartist":
        artist = client.dezapi.get_artist(id)
        keyboard = [
            [
                pyrogram.types.InlineKeyboardButton(text="Tracks 💿", switch_inline_query_current_chat=F".trks {artist['id']}"),
                pyrogram.types.InlineKeyboardButton(text="Albums 📼", switch_inline_query_current_chat=F".albs {artist['id']}")
            ],
            [pyrogram.types.InlineKeyboardButton(text="Delete 💣", callback_data="delete")]
        ]
        markup = pyrogram.types.InlineKeyboardMarkup(keyboard)
        await callback_query.message.reply_photo(photo=artist['picture_big'], caption=artist['name'], reply_markup=markup)
        await callback_query.answer(F"Went to {artist['name']}'s Info...")
    elif relate == "goalbum":
        album = client.dezapi.get_album(id)
        tracks = album['tracks']['data']
        keyboard = []
        counter = 1
        for track in tracks:
            key = [pyrogram.types.InlineKeyboardButton(F"{counter}. {track['title']} 💿", callback_data=F"download|{track['id']}")]
            keyboard.append(key)
            counter += 1
        keyboard.append([pyrogram.types.InlineKeyboardButton(F"Get all Tracks 💽", callback_data=F"getall|{album['id']}")])
        keyboard.append([pyrogram.types.InlineKeyboardButton(F"Go to Artist 👤", callback_data=F"goartist|{album['artist']['id']}")])
        keyboard.append([pyrogram.types.InlineKeyboardButton(text="Delete 💣", callback_data="delete")])
        markup = pyrogram.types.InlineKeyboardMarkup(keyboard)
        await callback_query.message.reply_photo(photo=album['cover_big'], caption=F"{album['title']} - {album['artist']['name']}", reply_markup=markup)
        await callback_query.answer(F"Went to {album['artist']['name']}'s {album['title']} Album...")
    elif relate == "getall":
        downloading = client.downloads.get(callback_query.message.from_user.id)
        if downloading:
            await callback_query.answer("You have to wait...")
            await callback_query.message.reply_text(text=F"You are currently downloading:\n{downloading}\nPlease wait for it to complete!")
        else:
            album = client.dezapi.get_album(id)
            tracks = album['tracks']['data']
            client.downloads[callback_query.message.from_user.id] = F"{album['title']} by {album['artist']['name']}"
            await callback_query.answer(F"Downloading {album['name']} album...")
            queue = await callback_query.message.reply_text(text=F"Uploading...")
            counter = 1
            for track in tracks:
                download = client.dezlog.download_trackdee(
                    track['link'],
                    output_dir=F"./musics/",
                    quality_download="MP3_128",
                    recursive_quality=True,
                    recursive_download=True,
                    method_save=1
                )
                await client.send_audio(chat_id=callback_query.message.chat.id, audio=download.song_path, title=track['title'], performer=track['artist']['name'], duration=track['duration'], progress=await client.progress(track['title'], queue, counter, len(tracks)), reply_markup=markup)
                os.remove(download.song_path)
                counter += 1
            await queue.delete()
            await callback_query.message.reply_text(text="Done!")
            del client.downloads[callback_query.message.from_user.id]
    elif relate == "download":
        track = client.dezapi.get_track(id)
        await callback_query.answer(F"Downloading {track['title']} track...")
        download = client.dezlog.download_trackdee(
            track['link'],
            output_dir=F"./musics/",
            quality_download="MP3_128",
            recursive_quality=True,
            recursive_download=True,
            method_save=1
        )
        await client.send_audio(chat_id=callback_query.message.chat.id, audio=download.song_path, title=track['title'], performer=track['artist']['name'], duration=track['duration'], reply_markup=markup)
        os.remove(download.song_path)
