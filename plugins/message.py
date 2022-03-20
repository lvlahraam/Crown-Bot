from pyrogram import Client, filters, types

@Client.on_message(filters.private | filters.regex("deezer.com") | filters.regex("spotify.com"))
async def search(client:Client, message:types.Message):
    text = message.text
    if "/" in text:
        items = text.split("/")
        if "deezer" in items[2]:
            if items[3] not in ("artist", "album", "track"):
                keyboard = [
                    [types.InlineKeyboardButton("Search Artist 👤", switch_inline_query_current_chat=".art ")],
                    [
                        types.InlineKeyboardButton("Search Album 📼", switch_inline_query_current_chat=".alb "),
                        types.InlineKeyboardButton("Search Track 💿", switch_inline_query_current_chat=".trk ")
                    ]
                ]
                markup = types.InlineKeyboardMarkup(keyboard)
                await message.reply_text(text="Invalid Deezer URL!", reply_markup=markup)
            elif items[3] == "artist":
                artist = client.dezapi.get_artist(items[4])
                keyboard = [
                    [
                        types.InlineKeyboardButton("Tracks 💿", switch_inline_query_current_chat=F".trks {artist['id']}"),
                        types.InlineKeyboardButton("Albums 📼", switch_inline_query_current_chat=F".albs {artist['id']}")
                    ]
                ]
                markup = types.InlineKeyboardMarkup(keyboard)
                await message.reply_photo(photo=artist['picture_big'], caption=F"{artist['name']}\n{artist['nb_album']}\n{artist['nb_fan']}", reply_markup=markup)
            elif items[3] == "album":
                album = client.dezapi.get_album(items[4])
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
                if len(tracks) > 1: keyboard.append([types.InlineKeyboardButton(F"Get All Tracks 💽", callback_data=F"getall|{album['id']}")])
                keyboard.append([types.InlineKeyboardButton(F"Go To Artist 👤", callback_data=F"goartist|{album['artist']['id']}")])
                markup = types.InlineKeyboardMarkup(keyboard)
                await message.reply_photo(photo=album['cover_big'], caption=F"{album['artist']['name']} - {album['title']}", reply_markup=markup)
            elif items[3] == "track":
                track = client.dezapi.get_track(items[4])
                keyboard = [
                    [
                        types.InlineKeyboardButton(F"{track['title']} 💿", callback_data=F"download|{track['id']}"),
                        types.InlineKeyboardButton(F"Get The Lyrics 📓", callback_data=F"lyrics|{track['id']}")
                    ],
                    [
                        types.InlineKeyboardButton(F"Go To Album 📼", callback_data=F"goalbum|{track['album']['id']}"),
                        types.InlineKeyboardButton(F"Go To Artist 👤", callback_data=F"goartist|{track['artist']['id']}")
                    ]
                ]
                markup = types.InlineKeyboardMarkup(keyboard)
                await message.reply_photo(photo=track['album']['cover_big'], caption=F"{track['artist']['name']} - {track['title']}", reply_markup=markup)
        # elif 
        else:
            await message.reply_text(text=F"Invalid {'spotify' if 'spotify'in items[2] else 'deezer'} url!\n\n1. The url must either be from deezer.com or spotify.com\n2. If your given url is a playlist:\nThis Bot will not download playlists, Due to the playlist might be a day long")
    else:
        keyboard = [
            [types.InlineKeyboardButton("Search Artist 👤", switch_inline_query_current_chat=F".art {text}")],
            [
                types.InlineKeyboardButton("Search Album 📼", switch_inline_query_current_chat=F".alb {text}"),
                types.InlineKeyboardButton("Search Track 💿", switch_inline_query_current_chat=F".trk {text}")
            ]
        ]
        markup = types.InlineKeyboardMarkup(keyboard)
        await message.reply_text(text=F"Searched: {text}", reply_markup=markup)