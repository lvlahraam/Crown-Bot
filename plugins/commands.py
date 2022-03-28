from pyrogram import Client, filters, types, errors

@Client.on_message(filters.command("start"))
async def start(client:Client, message:types.Message):
    await message.reply_text(text="Hi, I'm Crown, I can help you find the music you want\nTry my /help command to see what commands I've got")

@Client.on_message(filters.command("search"))
async def search(client:Client, message:types.Message):
    if len(message.command) > 1:
        query = message.command[1]
        text = F"Searched for {query}"
        keyboard = [
            [types.InlineKeyboardButton(text="Search Artist 👤", switch_inline_query_current_chat=F".art {query}")],
            [
                types.InlineKeyboardButton(text="Search Album 📼", switch_inline_query_current_chat=F".alb {query}"),
                types.InlineKeyboardButton(text="Search Track 💿", switch_inline_query_current_chat=F".trk {query}")
            ],
            [types.InlineKeyboardButton(text="Delete 💣", callback_data="delete")]
        ]
        markup = types.InlineKeyboardMarkup(keyboard)
    else:
        text = "You must pass an query"
        markup = None
    await message.reply_text(text=text, reply_markup=markup)

@Client.on_message(filters.command("info"))
async def info(client:Client, message:types.Message):
    try:
        if len(message.command) > 1:
            try:
                users = await client.get_users(message.command[1].split(", "))
                for user in users:
                    await message.reply_text(text=F"ID: {user.id}\nUser Name: {user.username}\nFirst Name: {user.first_name}\nLast name: {user.last_name}\nPhone Number: {user.phone_number}\nStatus: {user.status}\nMention: {user.mention}")
                await message.reply_text(text="Done!")
            except errors.UsernameNotOccupied as e:
                await message.reply_text(text=F"Couldn't find any user with this given info: {e.x}")
        else:
            await message.reply_text(text=F"ID: {message.from_user.id}\nUser Name: {message.from_user.username}\nFirst Name: {message.from_user.first_name}\nLast name: {message.from_user.last_name}\nPhone Number: {message.from_user.phone_number}\nStatus: {message.from_user.status}\nMention: {message.from_user.mention}")
    except errors.FloodWait as e:
        await message.reply_text(text=F"Wait '{e.x}' seconds before continuing!")

@Client.on_message(filters.command("help"))
async def help(client:Client, message:types.Message):
    keyboard = [
        [types.InlineKeyboardButton(text="Search Artist 👤", switch_inline_query_current_chat=".art ")],
        [
            types.InlineKeyboardButton(text="Search Album 📼", switch_inline_query_current_chat=".alb "),
            types.InlineKeyboardButton(text="Search Track 💿", switch_inline_query_current_chat=".trk ")
        ],
    ]
    markup = types.InlineKeyboardMarkup(keyboard)
    await message.reply_text(text="You can search for music by using the /search command\nAnd putting a search query in front of it for example:\n`/search Eminem`\n\nOr by sending a Deezer URL\nOr by tagging me in the text field and using:\n.art (as artist) - .alb (as album) - .trk (as track) tags and typing the query you want in front of it for example:\n`@crownmusicbot .alb Dawn Fm`\n\nOr even by using these buttons bellow\n\nFor artist's albums you could do:\n`@crownmusicbot .albs [artist's deezer id]`\nFor artist's tracks you could do:\n `@crownmusicbot .trks [artist's deezer id]`\nOr even by just searching for the artist and then click on albums or tracks button\n\nIf you wanted to see some information about yourself\nYou could try the /me command", reply_markup=markup)
