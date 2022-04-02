from pyrogram import Client, filters, types

@Client.on_message(filters.regex("deezer.com"))
async def message(client:Client, message:types.Message):
    text = message.text
    if "/" in text:
        items = text.split("/")
        if not len(items) >= 5:
            return await message.reply_text("Link must be for the artist or album or track!")
        relate = items[3]
        id = items[4]
    else:
        return await message.reply_text(text=F"Invalid Deezer URL!\n\n1. The url must be from deezer.com\n2. The url must be for a artist or a album or a track")
    if relate not in ("artist", "album", "track"):
        await message.reply_text(text="Invalid Deezer URL!", reply_markup=markup)
    elif relate == "artist":
        artist = client.dezapi.get_artist(id)
        keyboard = [
            [
                types.InlineKeyboardButton(text="Tracks 💿", switch_inline_query_current_chat=F".trks {artist['id']}"),
                types.InlineKeyboardButton(text="Albums 📼", switch_inline_query_current_chat=F".albs {artist['id']}")
            ],
            [types.InlineKeyboardButton(text="Delete 💣", callback_data="delete")]
        ]
        markup = types.InlineKeyboardMarkup(keyboard)
        await message.reply_photo(photo=artist['picture_big'], caption=artist['name'], reply_markup=markup)
    elif relate == "album":
        album = client.dezapi.get_album(id)
        tracks = album['tracks']['data']
        keyboard = []
        if len(tracks) > 1:
                counter = 1
                for track in tracks:
                    key = [types.InlineKeyboardButton(F"{counter}. {track['title']} 💿", callback_data=F"download|{track['id']}")]
                    keyboard.append(key)
                    counter += 1
        else:
            key = [types.InlineKeyboardButton(F"{tracks[0]['title']} 💿", callback_data=F"download|{tracks[0]['id']}")]
            keyboard.append(key)
        if len(tracks) > 1: keyboard.append([types.InlineKeyboardButton(F"Get all Tracks 💽", callback_data=F"getall|{album['id']}")])
        keyboard.append([types.InlineKeyboardButton(F"Go to Artist 👤", callback_data=F"goartist|{album['artist']['id']}")])
        keyboard.append([types.InlineKeyboardButton(text="Delete 💣", callback_data="delete")])
        markup = types.InlineKeyboardMarkup(keyboard)
        await message.reply_photo(photo=album['cover_big'], caption=F"{album['artist']['name']} - {album['title']}", reply_markup=markup)
    elif relate == "track":
        track = client.dezapi.get_track(id)
        keyboard = [
            [types.InlineKeyboardButton(F"{track['title']} 💿", callback_data=F"download|{track['id']}")],
            [
                types.InlineKeyboardButton(F"Go to Album 📼", callback_data=F"goalbum|{track['album']['id']}"),
                types.InlineKeyboardButton(F"Go to Artist 👤", callback_data=F"goartist|{track['artist']['id']}")
            ],
            [types.InlineKeyboardButton(text="Delete 💣", callback_data="delete")]
        ]
        markup = types.InlineKeyboardMarkup(keyboard)
        await message.reply_photo(photo=track['album']['cover_big'], caption=F"{track['artist']['name']} - {track['title']}", reply_markup=markup)
