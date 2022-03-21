import pyrogram

@pyrogram.Client.on_inline_query()
async def inline(client:pyrogram.Client, inline_query:pyrogram.types.InlineQuery):
    text = inline_query.query
    if text is None or not text.startswith("."): return
    query = " ".join(text.split(" ")[1:])
    if query is None: return
    results = []
    if text.startswith(".albs"):
        if query.isdigit():
              search = client.spotify.artist_albums(artist_id=query)
              datas = search['items']
        else:
            item = result = pyrogram.types.InlineQueryResultArticle(
                id="BADALBUMSSEARCH",
                title="Not an ID!",
                description="Query must be the artist's ID",
                input_message_content=pyrogram.types.InputTextMessageContent("/help")
            )
            return await inline_query.answer(results=[item])
    elif text.startswith(".trks"):
        if query.isdigit():
            search = client.spotify.artist_top_tracks(artist_id=query)
            datas = search['tracks']
        else:
            item = result = pyrogram.types.InlineQueryResultArticle(
                id="BADTRACKSSEARCH",
                title="Not an ID!",
                description="Query must be the artist's ID",
                input_message_content=pyrogram.types.InputTextMessageContent("/help")
            )
            return await inline_query.answer(results=[item])
    elif text.startswith(".art"):
        search = client.spotify.search(q=query, type="artist")
        datas = search['artists']['items']
    elif text.startswith(".alb"):
        search = client.spotify.search(q=query, type="album")
        datas = search['albums']['items']
    elif text.startswith(".trk"):
        search = client.spotify.search(q=query, type="track")
        datas = search['tracks']['items']
    added = []
    for data in datas:
        if data['type'] == "artist":
            description = data['followers']['total']
        elif data['type'] == "album":
            description = F"{data['artists'][0]['name']}\n{data['release_date']}\n{data['total_tracks']}"
        elif data['type'] == "track":
            description = F"{data['artists'][0]['name']}\n{data['album']['title']}\n{data['album']['release_date']}"
        if not data['id'] in added:
            result = pyrogram.types.InlineQueryResultArticle(
                id=data['id'],
                title=data['name'],
                description=description,
                thumb_url=data['images'][0]['url'],
                input_message_content=pyrogram.types.InputTextMessageContent(data['uri'])
            )
            if len(results) >= 50: break
            results.append(result)
            added.append(data['id'])
        else: pass
    await inline_query.answer(results)
