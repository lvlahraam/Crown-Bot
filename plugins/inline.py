import pyrogram

@pyrogram.Client.on_inline_query()
async def inline(client:pyrogram.Client, inline_query:pyrogram.types.InlineQuery):
    text = inline_query.query
    if text is None or not text.startswith(".") or not text.startswith(".art") or not text.startswith(".alb") or not text.startswith(".albs") or not text.startswith(".trk") or not text.startswith(".trks"):
        search = client.spotify.new_releases()
        datas = search['albums']['items']
    query = " ".join(text.split(" ")[1:])
    if text.startswith(".albs"):
        search = client.spotify.artist_albums(artist_id=query)
        datas = search['items']
    elif text.startswith(".trks"):
        search = client.spotify.artist_top_tracks(artist_id=query)
        datas = search['tracks']
    elif text.startswith(".art"):
        search = client.spotify.search(q=query, type="artist")
        datas = search['artists']['items']
    elif text.startswith(".alb"):
        search = client.spotify.search(q=query, type="album")
        datas = search['albums']['items']
    elif text.startswith(".trk"):
        search = client.spotify.search(q=query, type="track")
        datas = search['tracks']['items']
    results = []
    added = []
    for data in datas:
        if data['type'] == "artist":
            description = data['followers']['total']
            if len(data['images']) >= 1:
                thumbnail = data['images'][0]['url']
        elif data['type'] == "album":
            description = F"{data['artists'][0]['name']}\n{data['release_date']}\n{data['total_tracks']}"
            if len(data['images']) >= 1:
                thumbnail = data['images'][0]['url']
        elif data['type'] == "track":
            description = F"{data['artists'][0]['name']}\n{data['album']['name']}\n{data['album']['release_date']}"
            if len(data['album']['images']) >= 1:
                thumbnail = data['album']['images'][0]['url']
        result = pyrogram.types.InlineQueryResultArticle(
            id=data['id'],
            title=data['name'],
            description=description,
            thumb_url=thumbnail or None,
            input_message_content=pyrogram.types.InputTextMessageContent(data['uri'])
        )
        results.append(result)
        added.append(data['id'])
    await inline_query.answer(results)
