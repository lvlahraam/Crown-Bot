import pyrogram, string

@pyrogram.Client.on_inline_query()
async def inline(client:pyrogram.Client, inline_query:pyrogram.types.InlineQuery):
    text = inline_query.query.split(" ")
    option = text[0]
    query = " ".join(text[1:])
    results = []
    if option in (".art", ".alb", ".albs", ".trk", ".trks"):
        if not query.isspace():
            if option == ".art":
                search = client.dezapi.search_artist(query=query)        
            elif option == ".alb":
                search = client.dezapi.search_album(query=query)
            elif option == ".albs":
                if query.isdigit():
                    search = client.dezapi.get_artist_top_albums(query, limit=10)
                else:
                    item = result = pyrogram.types.InlineQueryResultArticle(
                        id="BADALBUMSSEARCH",
                        title="Not an ID!",
                        description="Query must be the artist's ID",
                        input_message_content=pyrogram.types.InputTextMessageContent("/help")
                    )
                    results.append(item)
            elif option == ".trk":
                search = client.dezapi.search_track(query=query)
            elif option == ".trks":
                if query.isdigit():
                    search = client.dezapi.get_artist_top_tracks(query, limit=10)
                else:
                    item = result = pyrogram.types.InlineQueryResultArticle(
                        id="BADALBUMSSEARCH",
                        title="Not an ID!",
                        description="Query must be the artist's ID",
                        input_message_content=pyrogram.types.InputTextMessageContent("/help")
                    )
                    results.append(item)
            datas = search['data']
            if len(datas) >= 1:
                added = []
                for data in datas:
                    if data['type'] == "artist":
                        name = data['name']
                        description = F"{data['nb_album']}\n{data['nb_fan']}"
                        thumbnail = data['picture']
                        add = data['name']
                    elif data['type'] == "album":
                        name = data['title']
                        description = F"{data.get('artist').get('name') if data.get('artist') else ''}\n{data.get('nb_tracks') or ''}\n{data.get('release_date') or ''}"
                        thumbnail = data['cover']
                        add = data.get('artist').get('name') if data.get('artist') else data['id']
                    elif data['type'] == "track":
                        name = data['title']
                        description = F"{data['artist']['name']}\n{data['album']['title']}\n{data.get('release_date') or ''}"
                        thumbnail = data['album']['cover']
                        add = data['id']
                    if not add in added:
                        result = pyrogram.types.InlineQueryResultArticle(
                            id=data['id'],
                            title=name,
                            description=description,
                            thumb_url=thumbnail,
                            input_message_content=pyrogram.types.InputTextMessageContent(data['link'])
                        )
                        results.append(result)
                        added.append(add)
                    else: pass
            else:
                result = pyrogram.types.InlineQueryResultArticle(
                    id="404",
                    title="Couldn't found anything",
                    description="Try to search for something else",
                    input_message_content=pyrogram.types.InputTextMessageContent("/help")
                )
                results.append(result)
        else:
                result = pyrogram.types.InlineQueryResultArticle(
                    id="INVALIDQUERY",
                    title="Query cannot be spaces",
                    description="You need to pass a valid query",
                    input_message_content=pyrogram.types.InputTextMessageContent("/help")
                )
                results.append(result)
    else:
        result = pyrogram.types.InlineQueryResultArticle(
            id="INVALIDTAGUSAGE",
            title="Not a Valid Tag",
            description="Usable tags: .art\n.alb - .albs\n.trk - .trks",
            input_message_content=pyrogram.types.InputTextMessageContent("/help")
        )
        results.append(result)
    await inline_query.answer(results=results)
