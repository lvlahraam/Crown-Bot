import pyrogram, spotipy, deezloader.deezloader, logging, os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
app = pyrogram.Client(session_name="crownmusicbot", bot_token=os.getenv("TOKEN"), api_id=os.getenv("API_ID"), api_hash=os.getenv("API_HASH"), plugins=dict(root="plugins")) 

app.spotify = spotipy.Spotify(auth_manager=spotipy.SpotifyClientCredentials(client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET")))

app.deezer = deezloader.deezloader.DeeLogin(arl=os.getenv("ARL"))

app.downloads = {}

async def progress(name:str, message:pyrogram.types.Message, current:int, total:int):
    await message.edit_text(F"Downloading: / {name} \ {current * 100 / total:.1f}%")
app.progress = progress

app.run()