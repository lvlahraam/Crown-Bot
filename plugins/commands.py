import pyrogram, io, textwrap, contextlib, traceback

@pyrogram.Client.on_message(pyrogram.filters.command("start"))
async def start(client:pyrogram.Client, message:pyrogram.types.Message):
    await message.reply_text(text="Hi, I'm Crown, I can help you find the music you want\nTry my /help command to see what commands I've got")

@pyrogram.Client.on_message(pyrogram.filters.command("help"))
async def help(client:pyrogram.Client, message:pyrogram.types.Message):
    keyboard = [
        [pyrogram.types.InlineKeyboardButton(text="Search Artist 👤", switch_inline_query_current_chat=".art ")],
        [
            pyrogram.types.InlineKeyboardButton(text="Search Album 📼", switch_inline_query_current_chat=".alb "),
            pyrogram.types.InlineKeyboardButton(text="Search Track 💿", switch_inline_query_current_chat=".trk ")
        ],
    ]
    markup = pyrogram.types.InlineKeyboardMarkup(keyboard)
    await message.reply_text(text="You can search for music by sending a message\nOr sending a Deezer URL\nOr by mentioning me in the chat and using:\n.art (as artist) - .alb (as album) - .trk (as track) tags and typing the query you want in front of it\nFor example: `@crownmusicbot .alb Dawn Fm`\n\nOr even by using these buttons bellow\n\nFor artist's albums you could do\nFor example: `@crownmusicbot .albs [artist's deezer id]`\nFor artist's tracks you could do\nFor example: `@crownmusicbot .trks [artist's deezer id]`\nOr even by just searching for the artist and then click on albums or tracks button\n\nIf you wanted to see some information about yourself\nYou could try the /me command", reply_markup=markup)

@pyrogram.Client.on_message(pyrogram.filters.command("me"))
async def me(client:pyrogram.Client, message:pyrogram.types.Message):
    me = message.from_user
    await message.reply_text(text=F"ID: {me.id}\nUser Name: {me.username}\nFirst Name: {me.first_name}\nLast name: {me.last_name}\nPhone Number: {me.phone_number}\nStatus: {me.status}\nMention: {me.mention}")

@pyrogram.Client.on_message(pyrogram.filters.command("commands") & pyrogram.filters.user(755341301))
async def commands(client:pyrogram.Client, message:pyrogram.types.Message):
    if len(message.command) > 1:
        items = message.command[1].split("/")
        botcommands = []
        for item in items:
            command = item.split(".")
            botcommands.append(pyrogram.types.BotCommand(command[0], command[2]))
        await client.set_bot_commands(botcommands)
        text = "Commands has been settled"
    else:
        await client.set_bot_commands(botcommands)
        text = "Commands has been removed"
    await message.reply_text(text=text)

@pyrogram.Client.on_message(pyrogram.filters.command("eval") & pyrogram.filters.user(755341301))
async def eval(client:pyrogram.Client, message:pyrogram.types.Message):
    env = {
        "pyrogram": pyrogram,
        "client": client,
        "message": message
    }
    body = message.command[1]
    env.update(globals())
    stdout = io.StringIO()
    to_compile = F"async def func():\n{textwrap.indent(body, '  ')}"
    try:
        exec(to_compile, env)
    except Exception as e:
        return await message.reply_text(text=F"`{e.__class__.__name__}: {e}`")
    func = env["func"]
    try:
        with contextlib.redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        await message.reply_text(text=F"`{value}{traceback.format_exc()}`")
    else:
        value = stdout.getvalue()
        try:
            await message.reply_text(text="\u2705")
        except:
            pass
        if ret is None:
            if value:
                await message.reply_text(text=F"`{value}`")
        else:
            await message.reply_text(text=F"`{value}{ret}`")
