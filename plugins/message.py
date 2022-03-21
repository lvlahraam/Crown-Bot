import pyrogram

@pyrogram.Client.on_message(pyrogram.filters.private | pyrogram.filters.regex("spotify"))
async def search(client:pyrogram.Client, message:pyrogram.types.Message):
    text = message.text
    if "spotify" in text:
        if "/" in text:
            items = text.split("/")
            relate = items[3]
            id = items[4]
        elif ":" in text:
            items = text.split(":")
            relate = items[1]
            id = items[2]
        else:
            await message.reply_text(text=F"Invalid Spotify URL!\n\n1. The url must be from spotify.com\n2. If your given url is a playlist:\nThis Bot will not download playlists, Due to the playlist might be a day long")
        if relate not in ("artist", "album", "track"):
            keyboard = [
                [pyrogram.types.InlineKeyboardButton(text="Search Artist 👤", switch_inline_query_current_chat=".art ")],
                [
                    pyrogram.types.InlineKeyboardButton(text="Search Album 📼", switch_inline_query_current_chat=".alb "),
                    pyrogram.types.InlineKeyboardButton(text="Search Track 💿", switch_inline_query_current_chat=".trk ")
                ]
            ]
            markup = pyrogram.types.InlineKeyboardMarkup(keyboard)
            await message.reply_text(text="Invalid Deezer URL!", reply_markup=markup)
        elif relate == "artist":
            artist = client.spoitfy.artist(id)
            keyboard = [
                [
                    pyrogram.types.InlineKeyboardButton(text="Tracks 💿", switch_inline_query_current_chat=F".trks {artist['id']}"),
                    pyrogram.types.InlineKeyboardButton(text="Albums 📼", switch_inline_query_current_chat=F".albs {artist['id']}")
                ]
            ]
            markup = pyrogram.types.InlineKeyboardMarkup(keyboard)
            await message.reply_photo(photo=artist["images"][0]["url"], caption=artist["name"], reply_markup=markup)
        elif relate == "album":
            album = client.spotify.album(id)
            tracks = album['tracks']['items']
            keyboard = []
            if len(tracks) > 1:
                counter = 1
                for track in tracks:
                    key = [pyrogram.types.InlineKeyboardButton(F"{track['track_number']}. {track['name']} 💿", callback_data=F"download|{track['id']}")]
                    keyboard.append(key)
                    counter += 1
            else:
                key = [pyrogram.types.InlineKeyboardButton(F"{tracks[0]['name']} 💿", callback_data=F"download|{tracks[0]['id']}")]
                keyboard.append(key)
            if len(tracks) > 1: keyboard.append([pyrogram.types.InlineKeyboardButton(F"Get all Tracks 💽", callback_data=F"getall|{album['id']}")])
            keyboard.append([pyrogram.types.InlineKeyboardButton(F"Go to Artist 👤", callback_data=F"goartist|{album['artists'][0]['id']}")])
            markup = pyrogram.types.InlineKeyboardMarkup(keyboard)
            await message.reply_photo(photo=album['images'][0]['url'], caption=F"{album['artists'][0]['name']} - {album['name']}", reply_markup=markup)
        elif relate == "track":
            track = client.spotify.track(id)
            keyboard = [
                [
                    pyrogram.types.InlineKeyboardButton(F"{track['name']} 💿", callback_data=F"download|{track['id']}"),
                    pyrogram.types.InlineKeyboardButton(F"Get the Lyrics 📓", callback_data=F"lyrics|{track['id']}")
                ],
                [
                    pyrogram.types.InlineKeyboardButton(F"Go to Album 📼", callback_data=F"goalbum|{track['album']['id']}"),
                    pyrogram.types.InlineKeyboardButton(F"Go to Artist 👤", callback_data=F"goartist|{track['artist']['id']}")
                ]
            ]
            markup = pyrogram.types.InlineKeyboardMarkup(keyboard)
            await message.reply_photo(photo=track['album']['images'][0]['url'], caption=F"{track['artists'][0]['name']} - {track['name']}", reply_markup=markup)
    else:
        keyboard = [
            [pyrogram.types.InlineKeyboardButton(text="Search Artist 👤", switch_inline_query_current_chat=F".art {text}")],
            [
                pyrogram.types.InlineKeyboardButton(text="Search Album 📼", switch_inline_query_current_chat=F".alb {text}"),
                pyrogram.types.InlineKeyboardButton(text="Search Track 💿", switch_inline_query_current_chat=F".trk {text}")
            ]
        ]
        markup = pyrogram.types.InlineKeyboardMarkup(keyboard)
        await message.reply_text(text=F"Searched: {text}", reply_markup=markup)
