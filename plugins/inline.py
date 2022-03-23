import pyrogram, string

@pyrogram.Client.on_inline_query()
async def inline(client:pyrogram.Client, inline_query:pyrogram.types.InlineQuery):
    text = inline_query.query.split(" ")
    option = text[0]
    query = " ".join(text[1:])
    if option in (".nwr", ".art", ".alb", ".albs", ".trk", ".trks"):
        if option == ".nwr":
                search = client.spotify.new_releases()
                datas = search['albums']['items']
        if not query.isspace():
            if option == ".art":
                search = client.spotify.search(q=query, type="artist")
                datas = search['artists']['items']
            elif option == ".alb":
                search = client.spotify.search(q=query, type="album")
                datas = search['albums']['items']
            elif option == ".albs":
                search = client.spotify.artist_albums(artist_id=query)
                datas = search['items']
            elif option == ".trk":
                search = client.spotify.search(q=query, type="track")
                datas = search['tracks']['items']
            elif option == ".trks":
                search = client.spotify.artist_top_tracks(artist_id=query)
                datas = search['tracks']
        results = []
        if len(datas) >= 1:
            added = []
            for data in datas:
                if data['type'] == "artist":
                    description = F"{data['followers']['total']}"
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
        else:
            result = pyrogram.types.InlineQueryResultArticle(
                id="404",
                title="Couldn't found anything",
                description="Try to search for something else",
                input_message_content=pyrogram.types.InputTextMessageContent("/help")
            )
            results.append(result)
        await inline_query.answer(results=results)
