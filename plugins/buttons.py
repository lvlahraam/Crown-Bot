import pyrogram, textwrap, os

@pyrogram.Client.on_callback_query()
async def buttons(client:pyrogram.Client, callback_query:pyrogram.types.CallbackQuery):
    query = callback_query
    data = query.data.split("|")
    relate = data[0]
    id = data[1]
    if relate == "lyrics":
        track = client.dezapi.get_track(id)
        lyrics = client.dezgw.get_lyric(id)
        wraps = textwrap.wrap(lyrics['LYRICS_TEXT'], width=1024)
        for wrapped in wraps:
            await query.message.reply_text(text=wrapped.replace("  ", "\n"))
        await query.answer(F"Here are the lyrics for {track['title']} track...")
    elif relate == "goartist":
        artist = client.dezapi.get_artist(id)
        keyboard = [
            [
                pyrogram.types.InlineKeyboardButton("Tracks 💿", switch_inline_query_current_chat=F".trks {artist['id']}"),
                pyrogram.types.InlineKeyboardButton("Albums 📼", switch_inline_query_current_chat=F".albs {artist['id']}")
            ]
        ]
        markup = pyrogram.types.InlineKeyboardMarkup(keyboard)
        await query.message.reply_photo(photo=artist['picture_big'], caption=artist['name'], reply_markup=markup)
        await query.answer(F"Went to {artist['name']}'s Info...")
    elif relate == "goalbum":
        album = client.dezapi.get_album(id)
        tracks = album['tracks']['data']
        keyboard = []
        ids = []
        counter = 1
        for track in tracks:
            if track['id'] in ids: pass
            else:
                key = [pyrogram.types.InlineKeyboardButton(F"{counter}. {track['title']} 💿", callback_data=F"download|{track['id']}")]
                keyboard.append(key)
                ids.append(track['id'])
                counter += 1
        keyboard.append([pyrogram.types.InlineKeyboardButton(F"Get all Tracks 💽", callback_data=F"getall|{album['id']}")])
        keyboard.append([pyrogram.types.InlineKeyboardButton(F"Go to Artist 👤", callback_data=F"goartist|{album['artist']['id']}")])
        markup = pyrogram.types.InlineKeyboardMarkup(keyboard)
        await query.message.reply_photo(photo=album['cover_big'], caption=F"{album['title']} - {album['artist']['name']}", reply_markup=markup)
        await query.answer(F"Went to {album['artist']['name']}'s {album['title']} Album...")
    elif relate == "getall":
        downloading = client.downloads.get(query.message.from_user.id)
        if downloading:
            await query.answer("You have to wait...")
            await query.message.reply_text(text=F"You are currently downloading:\n{downloading}\nPlease wait for it to complete!")
        else:
            album = client.dezapi.get_album(id)
            tracks = album['tracks']['data']
            client.downloads[query.message.from_user.id] = F"{album['title']} by {album['artist']['name']}"
            await query.answer(F"Downloading {album['title']} album...")
            queue = await query.message.reply_text(text=F"Downloading...")
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
                keyboard = [[pyrogram.types.InlineKeyboardButton("Get the Lyrics 📓", callback_data=F"lyrics|{track['id']}")]]
                markup = pyrogram.types.InlineKeyboardMarkup(keyboard)
                await client.send_audio(chat_id=query.message.chat.id, audio=download.song_path, title=track['title'], performer=track['artist']['name'], duration=track['duration'], progress=await client.progress(track['title'], queue, counter, len(tracks)), reply_markup=markup)
                os.remove(download.song_path)
                counter += 1
            await queue.delete()
            await query.message.reply_text("Done!")
            del client.downloads[query.message.from_user.id]
    elif relate == "download":
        track = client.dezapi.get_track(id)
        await query.answer(F"Downloading {track['title']} track...")
        download = client.dezlog.download_trackdee(
            track['link'],
            output_dir=F"./musics/",
            quality_download="MP3_128",
            recursive_quality=True,
            recursive_download=True,
            method_save=1
        )
        keyboard = [[pyrogram.types.InlineKeyboardButton("Get the Lyrics 📓", callback_data=F"lyrics|{track['id']}")]]
        markup = pyrogram.types.InlineKeyboardMarkup(keyboard)
        await client.send_audio(chat_id=query.message.chat.id, audio=download.song_path, title=track['title'], performer=track['artist']['name'], duration=track['duration'], reply_markup=markup)
        os.remove(download.song_path)
