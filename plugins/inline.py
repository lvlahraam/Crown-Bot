from pyrogram import Client, filters, types

@Client.on_inline_query()
async def inline(client:Client, inline_query:types.InlineQuery):
    text = inline_query.query
    if text is None or not text.startswith("."): return
    query = " ".join(text.split(" ")[1:])
    if query is None: return
    if text.startswith(".albs"):
        if query.isdigit():
            search = client.dezapi.get_artist_top_albums(query, limit=25)
        else:
            item = result = types.InlineQueryResultArticle(
                id="BADALBUMSSEARCH",
                title="Not an ID!",
                description="Query must be the artist's ID",
                input_message_content=types.InputTextMessageContent("/help")
            )
            return await inline_query.answer(results=[item])
    elif text.startswith(".trks"):
        if query.isdigit():
            search = client.dezapi.get_artist_top_tracks(query, limit=25)
        else:
            item = result = types.InlineQueryResultArticle(
                id="BADTRACKSSEARCH",
                title="Not an ID!",
                description="Query must be the artist's ID",
                input_message_content=types.InputTextMessageContent("/help")
            )
            return await inline_query.answer(results=[item])
    elif text.startswith(".art"):
        search = client.dezapi.search_artist(query=query)
    elif text.startswith(".alb"):
        search = client.dezapi.search_album(query=query)
    elif text.startswith(".trk"):
        search = client.dezapi.search_track(query=query)
    results = []
    added = []
    for data in search['data']:
        if data['type'] == "artist":
            name = data['name']
            description = F"{data['nb_album']}\n{data['nb_fan']}"
            thumbnail = data['picture']
            add = data['id']
        elif data['type'] == "album":
            name = data['title']
            artist = data.get("artist") or client.dezapi.get_artist(query)
            description = F"{artist['name']}\n{data.get('nb_tracks') or ''}\n{data.get('release_date') or ''}"
            thumbnail = data['cover']
            add = data['id']
        elif data['type'] == "track":
            name = data['title']
            description = F"{data['artist']['name']}\n{data['album']['title']}\n{data.get('release_date') or ''}"
            thumbnail = data['album']['cover']
            add = data['id']
        if not add in added:
            result = types.InlineQueryResultArticle(
                id=data['id'],
                title=name,
                description=description,
                thumb_url=thumbnail,
                input_message_content=types.InputTextMessageContent(data['link']),
            )
            if len(results) >= 50: break
            results.append(result)
            added.append(add)
        else: pass
    await inline_query.answer(results)