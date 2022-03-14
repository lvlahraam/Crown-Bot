# NOTE: THIS BOT DOES NOT DOWNLOAD ANY MUSIC ON THE DIRECTORY

import logging, os, pathlib, deezer
import deezloader.deezloader as deezloader
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, InputMediaPhoto
from telegram.ext import Updater, Filters, CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

dezclient = deezer.Client()
dezloader = deezloader.DeeLogin(email=os.getenv("EMAIL"), password=os.getenv("PASSWORD"))

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Search Arist 👤", switch_inline_query_current_chat=".art ")],
        [
            InlineKeyboardButton("Search Album 📀", switch_inline_query_current_chat=".alb "),
            InlineKeyboardButton("Search Track 📼", switch_inline_query_current_chat=".trk ")
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Hi\nI'm Crown", reply_markup=markup)

def help(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Search Arist 👤", switch_inline_query_current_chat=".art ")],
        [
            InlineKeyboardButton("Search Album 📀", switch_inline_query_current_chat=".alb "),
            InlineKeyboardButton("Search Track 📼", switch_inline_query_current_chat=".trk ")
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("You can search for music by sending a message\nOr by mentioning me in the chat and using:\n.art (as artist) - .alb (as album) - .trk (as track) and typing the query you want in front of it\nFor example: `@crownmusicbot .alb Dawn Fm`\n\nOr Even by using these buttons bellow", reply_markup=markup)

def searching(update: Update, context: CallbackContext):
    text = update.message.text
    if "/" in text:
        text = text.split("/")
        if text[3] == "artist":
            artist = dezclient.get_artist(text[4])
            keyboard = [
                [
                    InlineKeyboardButton("Top 10 Tracks", callback_data=F"top10|{artist.id}"),
                    InlineKeyboardButton("Albums", callback_data=F"albums|{artist.id}")
                ]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_photo(photo=artist.picture_medium, caption=F"{artist.name}\n{artist.nb_album}\n{artist.nb_fan}", reply_markup=markup)
        elif text[3] == "album":
            album = dezclient.get_album(text[4])
            tracks = album.get_tracks()
            keyboard = []
            counter = 1
            for track in tracks:
                key = [InlineKeyboardButton(F"{counter}. {track.title}", callback_data=F"download|{track.id}")]
                keyboard.append(key)
                counter += 1
            if len(tracks) > 1: keyboard.append([InlineKeyboardButton(F"Get All Tracks", callback_data=F"getall|{album.id}")])
            keyboard.append([InlineKeyboardButton(F"Go To Artist", callback_data=F"goartist|{album.artist.id}")])
            markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_photo(photo=album.cover_medium, caption=F"{album.artist.name} - {album.title}", reply_markup=markup)
    else:
        keyboard = [
            [InlineKeyboardButton("Search Arist 👤", switch_inline_query_current_chat=F".art {text}")],
            [
                InlineKeyboardButton("Search Album 📀", switch_inline_query_current_chat=F".alb {text}"),
                InlineKeyboardButton("Search Track 📼", switch_inline_query_current_chat=F".trk {text}")
            ]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(F"Searched: {text}", reply_markup=markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data.split("|")
    relate = data[0]
    id = data[1]
    if relate == "top10":
        artist = dezclient.get_artist(id)
        tracks = artist.get_top()[:10]
        keyboard = []
        ids = []
        counter = 1
        for track in tracks:
            if track.id in ids: pass
            else:
                key = [InlineKeyboardButton(F"{counter}. {track.title}", callback_data=F"download|{track.id}")]
                keyboard.append(key)
                ids.append(track.id)
                counter += 1
        keyboard.append([InlineKeyboardButton(F"Go To Artist", callback_data=F"goartist|{artist.id}")])
        markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_reply_markup(reply_markup=markup)
        query.answer(F"Here are the {artist.name}'s Top Tracks...")
    elif relate == "albums":
        artist = dezclient.get_artist(id)
        albums = artist.get_albums()
        keyboard = []
        ids = []
        counter = 1
        for album in albums:
            if album.id in ids: pass
            else:
                key = [InlineKeyboardButton(album.title, callback_data=F"goalbum|{album.id}")]
                keyboard.append(key)
                ids.append(album.id)
                counter += 1
        keyboard.append([InlineKeyboardButton(F"Go To Artist", callback_data=F"goartist|{artist.id}")])
        markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_reply_markup(reply_markup=markup)
        query.answer(F"Here are the {artist.name}'s Albums...")
    elif relate == "goartist":
        artist = dezclient.get_artist(id)
        keyboard = [
            [
                InlineKeyboardButton("Top 10 Tracks", callback_data=F"top10|{artist.id}"),
                InlineKeyboardButton("Albums", callback_data=F"albums|{artist.id}")
            ]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_media(media=InputMediaPhoto(media=artist.picture_medium))
        query.edit_message_caption(artist.name)
        query.edit_message_reply_markup(reply_markup=markup)
        query.answer(F"Went to {artist.name}'s Info...")
    elif relate == "goalbum":
        album = dezclient.get_album(id)
        tracks = album.get_tracks()
        keyboard = []
        ids = []
        counter = 1
        for track in tracks:
            if track.id in ids: pass
            else:
                key = [InlineKeyboardButton(F"{counter}. {track.title}", callback_data=F"download|{track.id}")]
                keyboard.append(key)
                ids.append(track.id)
                counter += 1
        keyboard.append([InlineKeyboardButton(F"Get All Tracks", callback_data=F"getall|{album.id}")])
        keyboard.append([InlineKeyboardButton(F"Go To Artist", callback_data=F"goartist|{album.artist.id}")])
        markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_photo(photo=album.cover_medium, caption=F"{album.artist.name} - {album.title}", reply_markup=markup)
        query.answer(F"Went to {album.artist.name}'s {album.title} Album...")
    elif relate == "download":
        track = dezclient.get_track(id)
        query.answer(F"Downloading {track.title} track...")
        download = dezloader.download_trackdee(
            track.link,
            output_dir=F"./musics/",
            quality_download="MP3_320",
            recursive_quality=True,
            recursive_download=True,
            method_save=2
        )
        query.message.reply_audio(audio=pathlib.Path(download.song_path).read_bytes(), duration=track.duration, performer=track.artist.name, title=track.title, thumb=track.album.cover_medium)
        os.remove(download.song_path)
    elif relate == "getall":
        album = dezclient.get_album(id)
        query.answer(F"Downloading {album.title} album...")
        download = dezloader.download_albumdee(
            album.link,
            output_dir=F"./musics/",
            quality_download="MP3_128",
            recursive_quality=True,
            recursive_download=True,
            method_save=2
        )
        query.message.reply_document(document=pathlib.Path(download.zip_path), caption=F"{album.artist.name} - {album.title}", thumb=album.cover_medium)
        os.remove(download.zip_path)

def inline(update: Update, context: CallbackContext):
    text = update.inline_query.query
    if not text or not text.startswith(".") or text == ".art" or text == ".art " or text == ".alb" or text == ".alb " or text == ".trk" or text == ".trk ": return
    if text.startswith(".art"):
        text = text.strip(".art ")
        search = dezclient.search_artists(query=text)
    elif text.startswith(".alb"):
        text = text.strip(".alb ")
        search = dezclient.search_albums(query=text)
    elif text.startswith(".trk"):
        text = text.strip(".trk ")
        search = dezclient.search_albums(query=text)
    results = []
    ids = []
    for data in search:
        if isinstance(data, deezer.Artist):
            title = data.name
            description = F"Albums: {data.nb_album}\nFans: {data.nb_fan}"
            thumbnail = data.picture
        elif isinstance(data, deezer.Album):
            title = data.title
            description = F"Artist: {data.artist.name}\nTracks: {data.nb_tracks}"
            thumbnail = data.cover
        elif isinstance(data, deezer.Track):
            title = data.title
            description = F"Artist: {data.artist.name}\nAlbum: {data.album.title}"
            thumbnail = data.md5_image
        if not data.id in ids:
            result = InlineQueryResultArticle(
                id=data.id,
                title=title,
                description=description,
                thumb_url=thumbnail,
                input_message_content=InputTextMessageContent(data.link),
            )
            if len(results) >= 50: break
            results.append(result)
            ids.append(data.id)
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

        updater.start_polling()
        updater.idle()
    except Exception as e:
        print(e)

main()
