import pyrogram

@pyrogram.Client.on_message(pyrogram.filters.private | pyrogram.filters.regex("deezer.com"))
async def search(client:pyrogram.Client, message:pyrogram.types.Message):
    text = message.text
    if "deezer.com" in text:
        if "/" in text:
            items = text.split("/")
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
                    pyrogram.types.InlineKeyboardButton(text="Tracks 💿", switch_inline_query_current_chat=F".trks {artist['id']}"),
                    pyrogram.types.InlineKeyboardButton(text="Albums 📼", switch_inline_query_current_chat=F".albs {artist['id']}")
                ],
                [pyrogram.types.InlineKeyboardButton(text="Delete 💣", callback_data="delete")]
            ]
            markup = pyrogram.types.InlineKeyboardMarkup(keyboard)
            await message.reply_photo(photo=artist['picture_big'], caption=artist['name'], reply_markup=markup)
        elif relate == "album":
            album = client.dezapi.get_album(id)
            tracks = album['tracks']['data']
            keyboard = []
            if len(tracks) > 1:
                    counter = 1
                    for track in tracks:
                        key = [pyrogram.types.InlineKeyboardButton(F"{counter}. {track['title']} 💿", callback_data=F"download|{track['id']}")]
                        keyboard.append(key)
                        counter += 1
            else:
                key = [pyrogram.types.InlineKeyboardButton(F"{tracks[0]['title']} 💿", callback_data=F"download|{tracks[0]['id']}")]
                keyboard.append(key)
            if len(tracks) > 1: keyboard.append([pyrogram.types.InlineKeyboardButton(F"Get all Tracks 💽", callback_data=F"getall|{album['id']}")])
            keyboard.append([pyrogram.types.InlineKeyboardButton(F"Go to Artist 👤", callback_data=F"goartist|{album['artist']['id']}")])
            keyboard.append([pyrogram.types.InlineKeyboardButton(text="Delete 💣", callback_data="delete")])
            markup = pyrogram.types.InlineKeyboardMarkup(keyboard)
            await message.reply_photo(photo=album['cover_big'], caption=F"{album['artist']['name']} - {album['title']}", reply_markup=markup)
        elif relate == "track":
            track = client.dezapi.get_track(id)
            keyboard = [
                [pyrogram.types.InlineKeyboardButton(F"{track['name']} 💿", callback_data=F"download|{track['id']}")],
                [
                    pyrogram.types.InlineKeyboardButton(F"Go to Album 📼", callback_data=F"goalbum|{track['album']['id']}"),
                    pyrogram.types.InlineKeyboardButton(F"Go to Artist 👤", callback_data=F"goartist|{track['artist']['id']}")
                ],
                [pyrogram.types.InlineKeyboardButton(text="Delete 💣", callback_data="delete")]
            ]
            markup = pyrogram.types.InlineKeyboardMarkup(keyboard)
            await message.reply_photo(photo=track['album']['cover_big'], caption=F"{track['artist']['name']} - {track['title']}", reply_markup=markup)
    else:
        keyboard = [
            [pyrogram.types.InlineKeyboardButton(text="Search Artist 👤", switch_inline_query_current_chat=F".art {text}")],
            [
                pyrogram.types.InlineKeyboardButton(text="Search Album 📼", switch_inline_query_current_chat=F".alb {text}"),
                pyrogram.types.InlineKeyboardButton(text="Search Track 💿", switch_inline_query_current_chat=F".trk {text}")
            ],
            [pyrogram.types.InlineKeyboardButton(text="Delete 💣", callback_data="delete")]
        ]
        markup = pyrogram.types.InlineKeyboardMarkup(keyboard)
        await message.reply_text(text=F"Searched: {text}", reply_markup=markup)
