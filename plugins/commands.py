from pyrogram import Client, filters, types

@Client.on_message(filters.command("start"))
async def start(client:Client, message:types.Message):
    keyboard = [
        [types.InlineKeyboardButton("Search Artist 👤", switch_inline_query_current_chat=".art ")],
        [
            types.InlineKeyboardButton("Search Album 📼", switch_inline_query_current_chat=".alb "),
            types.InlineKeyboardButton("Search Track 💿", switch_inline_query_current_chat=".trk ")
        ]
    ]
    markup = types.InlineKeyboardMarkup(keyboard)
    await message.reply_text(text="Hi\nI'm Crown", reply_markup=markup)

@Client.on_message(filters.command("help"))
async def help(client:Client, message:types.Message):
    keyboard = [
        [types.InlineKeyboardButton("Search Artist 👤", switch_inline_query_current_chat=".art ")],
        [
            types.InlineKeyboardButton("Search Album 📼", switch_inline_query_current_chat=".alb "),
            types.InlineKeyboardButton("Search Track 💿", switch_inline_query_current_chat=".trk ")
        ]
    ]
    markup = types.InlineKeyboardMarkup(keyboard)
    await message.reply_text(text="You can search for music by sending a message\nOr sending the deezer url\nOr by mentioning me in the chat and using:\n.art (as artist) - .alb (as album) - .trk (as track) and typing the query you want in front of it\nFor example: `@crownmusicbot .alb Dawn Fm`\n\nOr even by using these buttons bellow\n\nFor artist's albums you could do @crownmusicbot .albs [artist's deezer id]\nOr by just searching for the artist and then click on albums button", reply_markup=markup)