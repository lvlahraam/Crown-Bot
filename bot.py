# NOTE: THIS BOT DOES NOT DOWNLOAD ANY MUSIC ON THE DIRECTORY

import logging, os, pathlib, io, pydeezer
from telegram import Update, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, InputMediaPhoto
from telegram.ext import Updater, Filters, CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

deezer = pydeezer.Deezer(arl=os.getenv("ARL"))

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Search Artist 👤", switch_inline_query_current_chat=".art ")],
        [
            InlineKeyboardButton("Search Album 📀", switch_inline_query_current_chat=".alb "),
            InlineKeyboardButton("Search Track 📼", switch_inline_query_current_chat=".trk ")
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text="Hi\nI'm Crown", reply_markup=markup)

def help(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Search Artist 👤", switch_inline_query_current_chat=".art ")],
        [
            InlineKeyboardButton("Search Album 📀", switch_inline_query_current_chat=".alb "),
            InlineKeyboardButton("Search Track 📼", switch_inline_query_current_chat=".trk ")
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text="You can search for music by sending a message\nOr sending the deezer url\nOr by mentioning me in the chat and using:\n.art (as artist) - .alb (as album) - .trk (as track) and typing the query you want in front of it\nFor example: `@crownmusicbot .alb Dawn Fm`\n\nOr even by using these buttons bellow", reply_markup=markup)

def searching(update: Update, context: CallbackContext):
    text = update.message.text
    if "/" in text:
        text = text.split("/")
        if "deezer" not in text[2]:
            keyboard = [
	    	    [InlineKeyboardButton("Search Artist 👤", switch_inline_query_current_chat=".art ")],
	    	    [
			        InlineKeyboardButton("Search Album 📀", switch_inline_query_current_chat=".alb "),
		    	    InlineKeyboardButton("Search Track 📼", switch_inline_query_current_chat=".trk ")
	    	    ]
	        ]
            markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(text="The URL needs to be from Deezer!", reply_markup=markup)
        elif text[3] not in ("artist", "album"):
            keyboard = [
	    	    [InlineKeyboardButton("Search Artist 👤", switch_inline_query_current_chat=".art ")],
	    	    [
		            InlineKeyboardButton("Search Album 📀", switch_inline_query_current_chat=".alb "),
		            InlineKeyboardButton("Search Track 📼", switch_inline_query_current_chat=".trk ")
	    	    ]
	        ]
            markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(text="Invalid Deezer URL!", reply_markup=markup)
        elif text[3] == "artist":
            artist = deezer.get_artist(text[4])
            keyboard = [
                [
                    InlineKeyboardButton("Top 10 Tracks 🌟", callback_data=F"top10|{artist['DATA']['ART_ID']}"),
                    InlineKeyboardButton("Albums 📼", callback_data=F"albums|{artist['DATA']['ART_ID']}")
                ]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_photo(photo=deezer.get_artist_poster(artist)['image'], caption=F"{artist['DATA']['ART_NAME']}", reply_markup=markup)
        elif text[3] == "album":
            album = deezer.get_album(text[4])
            tracks = deezer.get_album_tracks(album['id'])
            keyboard = []
            if len(tracks) > 1:
                counter = 1
                for track in tracks:
                    key = [InlineKeyboardButton(F"{track['TRACK_NUMBER']}. {track['SNG_TITLE']} 📀", callback_data=F"download|{track['SNG_ID']}")]
                    keyboard.append(key)
                    counter += 1
            else:
                key = [InlineKeyboardButton(F"{tracks[0]['SNG_TITLE']} 📀", callback_data=F"download|{tracks[0]['SNG_ID']}")]
                keyboard.append(key)
            if len(tracks) > 1: keyboard.append([InlineKeyboardButton(F"Get All Tracks 💣", callback_data=F"getall|{album['id']}")])
            keyboard.append([InlineKeyboardButton(F"Go To Artist 👤", callback_data=F"goartist|{album['artist']['id']}")])
            markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_photo(photo=album['cover_big'], caption=F"{album['artist']['name']} - {album['title']}", reply_markup=markup)
    else:
        keyboard = [
            [InlineKeyboardButton("Search Artist 👤", switch_inline_query_current_chat=F".art {text}")],
            [
                InlineKeyboardButton("Search Album 📀", switch_inline_query_current_chat=F".alb {text}"),
                InlineKeyboardButton("Search Track 📼", switch_inline_query_current_chat=F".trk {text}")
            ]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(text=F"Searched: {text}", reply_markup=markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data.split("|")
    relate = data[0]
    id = data[1]
    if relate == "top10":
        artist = deezer.get_artist(id)
        tracks = deezer.get_artist_top_tracks(artist["DATA"]['ART_ID'])
        keyboard = []
        ids = []
        counter = 1
        for track in tracks:
            if counter == 11: break
            if track['SNG_ID'] in ids: pass
            else:
                key = [InlineKeyboardButton(F"{track['TRACK_NUMBER']}. {track['SNG_TITLE']} [{track['ALB_TITLE']}]📀", callback_data=F"download|{track['SNG_ID']}")]
                keyboard.append(key)
                ids.append(track['SNG_ID'])
                counter += 1
        keyboard.append([InlineKeyboardButton(F"Go To Artist 👤", callback_data=F"goartist|{artist['DATA']['ART_ID']}")])
        markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_reply_markup(reply_markup=markup)
        query.answer(F"Here are the {artist['DATA']['ART_NAME']}'s Top Tracks...")
    elif relate == "albums":
        artist = deezer.get_artist(id)
        albums = artist['ALBUMS']['data']
        keyboard = []
        titles = []
        for album in albums:
            if album['ALB_TITLE'] in titles: pass
            else:
                key = [InlineKeyboardButton(F"{album['ALB_TITLE']} 📼", callback_data=F"goalbum|{album['ALB_ID']}")]
                keyboard.append(key)
                titles.append(album['ALB_TITLE'])
        keyboard.append([InlineKeyboardButton(F"Go To Artist 👤", callback_data=F"goartist|{artist['DATA']['ART_ID']}")])
        markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_reply_markup(reply_markup=markup)
        query.answer(F"Here are the {artist['DATA']['ART_NAME']}'s Albums...")
    elif relate == "goartist":
        artist = deezer.get_artist(id)
        keyboard = [
            [
                InlineKeyboardButton("Top 10 Tracks 🌟", callback_data=F"top10|{artist['DATA']['ART_ID']}"),
                InlineKeyboardButton("Albums 📼", callback_data=F"albums|{artist['DATA']['ART_ID']}")
            ]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_media(media=InputMediaPhoto(media=io.BytesIO.read(deezer.get_artist_poster(artist)['image'])))
        query.edit_message_caption(artist["DATA"]["ART_NAME"])
        query.edit_message_reply_markup(reply_markup=markup)
        query.answer(F"Went to {artist['DATA']['ART_NAME']}'s Info...")
    elif relate == "goalbum":
        album = deezer.get_album(id)
        tracks = deezer.get_album_tracks(album['id'])
        keyboard = []
        ids = []
        counter = 1
        for track in tracks:
            if track['SNG_ID'] in ids: pass
            else:
                key = [InlineKeyboardButton(F"{track['TRACK_NUMBER']}. {track['SNG_TITLE']} 📀", callback_data=F"download|{track['SNG_ID']}")]
                keyboard.append(key)
                ids.append(track['SNG_ID'])
                counter += 1
        keyboard.append([InlineKeyboardButton(F"Get All Tracks 💣", callback_data=F"getall|{album['id']}")])
        keyboard.append([InlineKeyboardButton(F"Go To Artist 👤", callback_data=F"goartist|{album['artist']['id']}")])
        markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_photo(photo=album['cover_big'], caption=F"{album['artist']['name']} - {album['title']}", reply_markup=markup)
        query.answer(F"Went to {album['artist']['name']}'s {album['title']} Album...")
    elif relate == "getall":
        album = deezer.get_album(id)
        tracks = deezer.get_album_tracks(album['id'])
        query.answer(F"Downloading {album['title']} album... One Track!")
        query.delete_message()
        downloads = []
        for track in tracks:
            downloads.append(track["SNG_ID"])
        download = pydeezer.Downloader(deezer, downloads, "./musics")
        print(download.download_dir)
    elif relate == "download":
        album = deezer.get_album(track['info']['DATA']['ALB_ID'])
        track = deezer.get_track(id)
        query.answer(F"Downloading {track['SNG_TITLE']} track...")
        download = deezer.download_track(track, "./musics/", quality=pydeezer.constants.track_formats.MP3_320, with_lyrics=True)
        print(download)
        # query.message.reply_audio(audio=, duration=track['info']['DATA']['DURATION'], performer=track['info']['DATA']['ART_NAME'], title=track['info']['DATA']['SNG_TITLE'], thumb=io.BytesIO.read(deezer.get_album_poster(album)['image']))

def inline(update: Update, context: CallbackContext):
    text = update.inline_query.query
    if not text or not text.startswith(".") or text == ".art" or text == ".art " or text == ".alb" or text == ".alb " or text == ".trk" or text == ".trk ": return
    if text.startswith(".art"):
        text = text.strip(".art ")
        search = deezer.search_artists(query=text)
    elif text.startswith(".alb"):
        text = text.strip(".alb ")
        search = deezer.search_albums(query=text)
    elif text.startswith(".trk"):
        text = text.strip(".trk ")
        search = deezer.search_tracks(query=text)
    results = []
    ids = []
    for data in search:
        if data['type'] == "artist":
            title = data['name']
            description = F"Albums: {data['nb_album']}\nFans: {data['nb_fan']}"
            thumbnail = data['picture']
        elif data['type'] == "album":
            title = data['title']
            description = F"Artist: {data['artist']['name']}\nTracks: {data['nb_tracks']}"
            thumbnail = data['cover']
        elif data['type'] == "track":
            title = data['title']
            description = F"Artist: {data['artist']['name']}\nAlbum: {data['album']['title']}"
            thumbnail = data['album']['cover']
        if not data['id'] in ids:
            result = InlineQueryResultArticle(
                id=data['id'],
                title=title,
                description=description,
                thumb_url=thumbnail,
                input_message_content=InputTextMessageContent(data['link']),
            )
            if len(results) >= 50: break
            results.append(result)
            ids.append(data['id'])
        else: pass
    update.inline_query.answer(results)

def error(update: Update, context: CallbackContext):
    logger.warning(F"Update: {update}\n\nCaused: {context.error}")

def main():
    try:
        updater = Updater(os.getenv("TOKEN"))

        print(F"Hello I'm: {updater.bot.name}")

        updater.dispatcher.add_handler(CommandHandler("start", start))
        updater.dispatcher.add_handler(CommandHandler("help", help))
        updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, searching))
        updater.dispatcher.add_handler(CallbackQueryHandler(button))
        updater.dispatcher.add_handler(InlineQueryHandler(inline))

        commands = [
            BotCommand("start", "Starts the bot"),
            BotCommand("help", "Helps you to use the bot"),
        ]
        updater.bot.set_my_commands(commands)
        
        updater.start_polling()
        updater.idle()
    except Exception as e:
        print(e)

main()
