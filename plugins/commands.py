import pyrogram

@pyrogram.Client.on_message(pyrogram.filters.command("start"))
async def start(client:pyrogram.Client, message:pyrogram.types.Message):
    keyboard = [
        [pyrogram.types.InlineKeyboardButton("Search Artist 👤", switch_inline_query_current_chat=".art ")],
        [
            pyrogram.types.InlineKeyboardButton("Search Album 📼", switch_inline_query_current_chat=".alb "),
            pyrogram.types.InlineKeyboardButton("Search Track 💿", switch_inline_query_current_chat=".trk ")
        ]
    ]
    markup = pyrogram.types.InlineKeyboardMarkup(keyboard)
    await message.reply_text(text="Hi\nI'm Crown", reply_markup=markup)

@pyrogram.Client.on_message(pyrogram.filters.command("help"))
async def help(client:pyrogram.Client, message:pyrogram.types.Message):
    keyboard = [
        [pyrogram.types.InlineKeyboardButton("Search Artist 👤", switch_inline_query_current_chat=".art ")],
        [
            pyrogram.types.InlineKeyboardButton("Search Album 📼", switch_inline_query_current_chat=".alb "),
            pyrogram.types.InlineKeyboardButton("Search Track 💿", switch_inline_query_current_chat=".trk ")
        ]
    ]
    markup = pyrogram.types.InlineKeyboardMarkup(keyboard)
    await message.reply_text(text="You can search for music by sending a message\nOr sending the deezer url\nOr by mentioning me in the chat and using:\n.art (as artist) - .alb (as album) - .trk (as track) and typing the query you want in front of it\nFor example: `@crownmusicbot .alb Dawn Fm`\n\nOr even by using these buttons bellow\n\nFor artist's albums you could do\nFor example: `@crownmusicbot .albs [artist's deezer id]`\nFor artist's tracks you could do\nFor example: `@crownmusicbot .trks [artist's deezer id]\nOr even by just searching for the artist and then click on albums or tracks button", reply_markup=markup)

@pyrogram.Client.on_message(pyrogram.filters.command("me"))
async def me(client:pyrogram.Client, message:pyrogram.types.Message):
    me = message.from_user
    await message.reply_text(text=F"ID: {me.id}\nUser Name: {me.username}\nFirst Name: {me.first_name}\nLast name: {me.last_name}\nPhone Number: {me.phone_number}\nStatus: {me.status}\nMention: {me.mention}")