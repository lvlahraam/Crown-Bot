import textwrap, pathlib, os,  wget
from pyrogram import Client, filters, types

@Client.on_callback_query()
async def buttons(client:Client, callback_query:types.CallbackQuery):
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
                types.InlineKeyboardButton("Tracks 💿", switch_inline_query_current_chat=F".trks {artist['id']}"),
                types.InlineKeyboardButton("Albums 📼", switch_inline_query_current_chat=F".albs {artist['id']}")
            ]
        ]
        markup = types.InlineKeyboardMarkup(keyboard)
        await query.edit_message_media(media=types.InputMedia(media=artist['picture_big'], caption=artist['name']), reply_markup=markup)
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
                key = [types.InlineKeyboardButton(F"{counter}. {track['title']} 💿", callback_data=F"download|{track['id']}")]
                keyboard.append(key)
                ids.append(track['id'])
                counter += 1
        keyboard.append([types.InlineKeyboardButton(F"Get All Tracks 💽", callback_data=F"getall|{album['id']}")])
        keyboard.append([types.InlineKeyboardButton(F"Go To Artist 👤", callback_data=F"goartist|{album['artist']['id']}")])
        markup = types.InlineKeyboardMarkup(keyboard)
        await query.edit_message_media(photo=types.InputMedia(media=album['cover_big'], caption=F"{album['artist']['name']} - {album['title']}"), reply_markup=markup)
        await query.answer(F"Went to {album['artist']['name']}'s {album['title']} Album...")
    elif relate == "getall":
        downloading = client.downloads.get(query.message.from_user.id)
        if downloading:
            await query.answer("You have to wait...")
            await query.message.reply_text(text=F"You are currently downloading:\n{downloading}\nPlease wait for it to complete!")
        else:
            album = client.dezapi.get_album(id)
            tracks = album['tracks']['data']
            image = wget.download(track['album']['cover_big'])
            client.downloads[query.message.from_user.id] = F"{album['title']} by {album['artist']['name']}"
            await query.answer(F"Downloading {album['title']} album...")
            queue = await query.message.reply_text(text=F"Downloading {album['title']} album tracks...\n{len(tracks)} left...")
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
                await queue.edit_text(text=F"Downloading {track['title']} track...\n{counter}/{len(tracks)} left...")
                await query.message.reply_audio(audio=pathlib.Path(download.song_path).read_bytes(), title=track['title'], performer=album['artist']['name'], duration=track['duration'], thumb=F"./{image}")
                os.remove(download.song_path)
                counter += 1
            await query.message.reply_text("Done!")
            del client.downloads[query.message.from_user.id]
            os.remove(F"./{image}")
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
        image = wget.download(track['album']['cover_big'])
        await query.message.reply_audio(audio=pathlib.Path(download.song_path).read_bytes(), title=track['title'], performer=track['artist']['name'], duration=track['duration'], thumb=F"./{image}")
        os.remove(download.song_path)
        os.remove(F"./{image}")