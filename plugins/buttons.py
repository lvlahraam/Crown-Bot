import pyrogram, textwrap, os

@pyrogram.Client.on_callback_query()
async def buttons(client:pyrogram.Client, callback_query:pyrogram.types.CallbackQuery):
    query = callback_query
    data = query.data.split("|")
    relate = data[0]
    id = data[1]
    if relate == "lyrics":
        track = client.spotify.track(id)
        lyrics = client.dezgw.get_lyric(id)
        wraps = textwrap.wrap(lyrics['LYRICS_TEXT'], width=1024)
        for wrapped in wraps:
            await query.message.reply_text(text=wrapped.replace("  ", "\n"))
        await query.answer(F"Here are the lyrics for {track['name']} track...")
    elif relate == "goartist":
        artist = client.spotify.artist(id)
        keyboard = [
            [
                pyrogram.types.InlineKeyboardButton(text="Tracks 💿", switch_inline_query_current_chat=F".trks {artist['id']}"),
                pyrogram.types.InlineKeyboardButton(text="Albums 📼", switch_inline_query_current_chat=F".albs {artist['id']}")
            ]
        ]
        markup = pyrogram.types.InlineKeyboardMarkup(keyboard)
        await query.message.reply_photo(photo=artist['images'][0]['url'], caption=artist['name'], reply_markup=markup)
        await query.answer(F"Went to {artist['name']}'s Info...")
    elif relate == "goalbum":
        album = client.spotify.album(id)
        tracks = album['tracks']['item']
        keyboard = []
        ids = []
        counter = 1
        for track in tracks:
            if track['id'] in ids: pass
            else:
                key = [pyrogram.types.InlineKeyboardButton(F"{track['track_number']}. {track['name']} 💿", callback_data=F"download|{track['id']}")]
                keyboard.append(key)
                ids.append(track['id'])
                counter += 1
        keyboard.append([pyrogram.types.InlineKeyboardButton(F"Get all Tracks 💽", callback_data=F"getall|{album['id']}")])
        keyboard.append([pyrogram.types.InlineKeyboardButton(F"Go to Artist 👤", callback_data=F"goartist|{album['artists'][0]['id']}")])
        markup = pyrogram.types.InlineKeyboardMarkup(keyboard)
        await query.message.reply_photo(photo=album['images'][0]['url'], caption=F"{album['name']} - {album['artists'][0]['name']}", reply_markup=markup)
        await query.answer(F"Went to {album['artists'][0]['name']}'s {album['name']} Album...")
    elif relate == "getall":
        downloading = client.downloads.get(query.message.from_user.id)
        if downloading:
            await query.answer("You have to wait...")
            await query.message.reply_text(text=F"You are currently downloading:\n{downloading}\nPlease wait for it to complete!")
        else:
            album = client.spotify.album(id)
            tracks = album['tracks']['items']
            client.downloads[query.message.from_user.id] = F"{album['name']} by {album['artists'][0]['name']}"
            await query.answer(F"Downloading {album['name']} album...")
            queue = await query.message.reply_text(text=F"Downloading...")
            counter = 1
            for track in tracks:
                download = client.deezer.download_trackspo(
                    track['uri'].replace(":", "/").replace("spotify", "https://open.spotify.com"),
                    output_dir=F"./musics/",
                    quality_download="MP3_128",
                    recursive_quality=True,
                    recursive_download=True,
                    method_save=1
                )
                keyboard = [[pyrogram.types.InlineKeyboardButton(text="Get the Lyrics 📓", callback_data=F"lyrics|{track['id']}")]]
                markup = pyrogram.types.InlineKeyboardMarkup(keyboard)
                await client.send_audio(chat_id=query.message.chat.id, audio=download.song_path, title=track['name'], performer=track['artists'][0]['name'], duration=track['duration_ms'], progress=await client.progress(track['name'], queue, counter, len(tracks)), reply_markup=markup)
                os.remove(download.song_path)
                counter += 1
            await queue.delete()
            await query.message.reply_text(text="Done!")
            del client.downloads[query.message.from_user.id]
    elif relate == "download":
        track = client.spotify.track(id)
        await query.answer(F"Downloading {track['name']} track...")
        download = client.deezer.download_trackspo(
            track['uri'].replace(":", "/").replace("spotify", "https://open.spotify.com"),
            output_dir=F"./musics/",
            quality_download="MP3_128",
            recursive_quality=True,
            recursive_download=True,
            method_save=1
        )
        keyboard = [[pyrogram.types.InlineKeyboardButton(text="Get the Lyrics 📓", callback_data=F"lyrics|{track['id']}")]]
        markup = pyrogram.types.InlineKeyboardMarkup(keyboard)
        await client.send_audio(chat_id=query.message.chat.id, audio=download.song_path, title=track['name'], performer=track['artists'][0]['name'], duration=track['duration_ms'], reply_markup=markup)
        os.remove(download.song_path)
