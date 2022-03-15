# NOTE: THIS BOT DOES NOT DOWNLOAD ANY MUSIC ON THE DIRECTORY

import logging, os, pathlib, deezer
from deezloader import deezloader
from telegram import Update, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, InputMediaPhoto
from telegram.ext import Updater, Filters, CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

dezclient = deezer.Client()
dezloader = deezloader.DeeLogin(arl=os.getenv("ARL"))

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
    update.message.reply_text(text="You can search for music by sending a message\nOr sending the deezer url\nOr by mentioning me in the chat and using:\n.art (as artist) - .alb (as album) - .trk (as track) and typing the query you want in front of it\nFor example: `@crownmusicbot .alb Dawn Fm`\n\nOr even by using these buttons bellow\n\nFor artist's albums you could do @crownmusicbot .albs [artist's deezer id]\nOr by just searching for the artist and then click on albums button", reply_markup=markup)

def searching(update: Update, context: CallbackContext):
    text = update.message.text
    if "/" in text:
        items = text.split("/")
        if "deezer" in items[2]:
            if items[3] not in ("artist", "album"):
                keyboard = [
                    [InlineKeyboardButton("Search Artist 👤", switch_inline_query_current_chat=".art ")],
                    [
                        InlineKeyboardButton("Search Album 📀", switch_inline_query_current_chat=".alb "),
                        InlineKeyboardButton("Search Track 📼", switch_inline_query_current_chat=".trk ")
                    ]
                ]
                markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text(text="Invalid Deezer URL!", reply_markup=markup)
            elif items[3] == "artist":
                artist = dezclient.get_artist(items[4])
                keyboard = [
                    [
                        InlineKeyboardButton("Top 10 Tracks 🌟", callback_data=F"top10|{artist.id}"),
                        InlineKeyboardButton("Albums 📼", switch_inline_query_current_chat=F".albs {artist.id}")
                    ]
                ]
                markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_photo(photo=artist.picture_big, caption=F"{artist.name}\n{artist.nb_album}\n{artist.nb_fan}", reply_markup=markup)
            elif items[3] == "album":
                album = dezclient.get_album(items[4])
                tracks = album.get_tracks()
                keyboard = []
                if len(tracks) > 1:
                    counter = 1
                    for track in tracks:
                        key = [InlineKeyboardButton(F"{counter}. {track.title} 📀", callback_data=F"download|{track.id}")]
                        keyboard.append(key)
                        counter += 1
                else:
                    key = [InlineKeyboardButton(F"{tracks[0].title} 📀", callback_data=F"download|{tracks[0].id}")]
                    keyboard.append(key)
                if len(tracks) > 1: keyboard.append([InlineKeyboardButton(F"Get All Tracks 💣", callback_data=F"getall|{album.id}")])
                keyboard.append([InlineKeyboardButton(F"Go To Artist 👤", callback_data=F"goartist|{album.artist.id}")])
                markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_photo(photo=album.cover_big, caption=F"{album.artist.name} - {album.title}", reply_markup=markup)
        else:
            update.message.reply_text(text=F"Invalid {'spotify' if 'spotify'in items[2] else 'deezer'} url!\n\n1. The url must either be from deezer.com or spotify.com\n2. If your given url is a playlist:\nThis Bot will not download playlists, Due to the playlist might be a day long")
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
        artist = dezclient.get_artist(id)
        tracks = artist.get_top()[:10]
        keyboard = []
        ids = []
        counter = 1
        for track in tracks:
            if track.id in ids: pass
            else:
                key = [InlineKeyboardButton(F"{counter}. {track.title} 📀", callback_data=F"download|{track.id}")]
                keyboard.append(key)
                ids.append(track.id)
                counter += 1
        keyboard.append([InlineKeyboardButton(F"Go To Artist 👤", callback_data=F"goartist|{artist.id}")])
        markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_reply_markup(reply_markup=markup)
        query.answer(F"Here are the {artist.name}'s Top Tracks...")
    elif relate == "albums":
        artist = dezclient.get_artist(id)
        albums = artist.get_albums()
        keyboard = []
        titles = []
        counter = 1
        for album in albums:
            if album.title in titles: pass
            else:
                key = [InlineKeyboardButton(F"{album.title} 📼", callback_data=F"goalbum|{album.id}")]
                keyboard.append(key)
                titles.append(album.title)
                counter += 1
        keyboard.append([InlineKeyboardButton(F"Go To Artist 👤", callback_data=F"goartist|{artist.id}")])
        markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_reply_markup(reply_markup=markup)
        query.answer(F"Here are the {artist.name}'s Albums...")
    elif relate == "goartist":
        artist = dezclient.get_artist(id)
        keyboard = [
            [
                InlineKeyboardButton("Top 10 Tracks 🌟", callback_data=F"top10|{artist.id}"),
                InlineKeyboardButton("Albums 📼", switch_inline_query_current_chat=F".albs {artist.id}")
            ]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_media(media=InputMediaPhoto(media=artist.picture_big))
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
                key = [InlineKeyboardButton(F"{counter}. {track.title} 📀", callback_data=F"download|{track.id}")]
                keyboard.append(key)
                ids.append(track.id)
                counter += 1
        keyboard.append([InlineKeyboardButton(F"Get All Tracks 💣", callback_data=F"getall|{album.id}")])
        keyboard.append([InlineKeyboardButton(F"Go To Artist 👤", callback_data=F"goartist|{album.artist.id}")])
        markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_photo(photo=album.cover_big, caption=F"{album.artist.name} - {album.title}", reply_markup=markup)
        query.answer(F"Went to {album.artist.name}'s {album.title} Album...")
    elif relate == "getall":
        album = dezclient.get_album(id)
        tracks = album.get_tracks()
        query.answer(F"Downloading {album.title} album...")
        query.delete_message()
        for track in tracks:
            download = dezloader.download_trackdee(
                track.link,
                output_dir=F"./musics/",
                quality_download="MP3_128",
                recursive_quality=True,
                recursive_download=True,
                method_save=1
            )
            query.answer(F"Downloaded {track.title} track...")
            query.message.reply_audio(audio=pathlib.Path(download.song_path).read_bytes(), filename=F"{track.artist} - {track.title}", title=track.title, performer=track.artist.name, duration=track.duration, thumb=track.album.cover_big, timeout=30)
        query.message.reply_text("Done!")
    elif relate == "download":
        track = dezclient.get_track(id)
        query.answer(F"Downloading {track.title} track...")
        download = dezloader.download_trackdee(
            track.link,
            output_dir=F"./musics/",
            quality_download="MP3_128",
            recursive_quality=True,
            recursive_download=True,
            method_save=1
        )
        query.message.reply_audio(audio=pathlib.Path(download.song_path).read_bytes(), filename=F"{track.artist} - {track.title}", title=track.title, performer=track.artist.name, duration=track.duration, thumb=track.album.cover_big, timeout=30)

def inline(update: Update, context: CallbackContext):
    text = update.inline_query.query
    if text is None or not text.startswith("."): return
    query = text.strip(".albs ").strip(".art ").strip(".alb ").strip(".trk ")
    if query is None: return
    if text.startswith(".albs"):
        if text.isdigit():
            artist = dezclient.get_artist(text)
            search = artist.get_albums()
        else:
            item = result = InlineQueryResultArticle(
                id="BADALBUMSSEARCH",
                title="Not an ID!",
                description="Query must be the artist's ID",
                input_message_content=InputTextMessageContent("/help")
            )
            return update.inline_query.answer(results=[item])
    elif text.startswith(".art"):
        search = dezclient.search_artists(query=text)
    elif text.startswith(".alb"):
        search = dezclient.search_albums(query=text)
    elif text.startswith(".trk"):
        search = dezclient.search_albums(query=text)
    results = []
    ids = []
    for data in search:
        if isinstance(data, deezer.Artist):
            title = data.name
            description = data.nb_album
            thumbnail = data.picture
        elif isinstance(data, deezer.Album):
            title = data.title
            description = data.artist.name
            thumbnail = data.cover
        elif isinstance(data, deezer.Track):
            title = data.title
            description = F"{data.artist.name}\n{data.album.title}"
            thumbnail = data.album.cover
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
        updater = Updater(token=os.getenv("TOKEN"))

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
