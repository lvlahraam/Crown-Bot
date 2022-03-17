import asyncio, logging, os, aiohttp
from deezloader.deezloader import DeeLogin, API, API_GW
import pyrogram

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

app = pyrogram.Client(session_name="crownmusicbot", bot_token=os.getenv("TOKEN"), api_id=os.getenv("API_ID"), api_hash=os.getenv("API_HASH"), plugins=dict(root="plugins")) 

app.dezlog = DeeLogin(arl=os.getenv("ARL"))
app.dezapi = API()
app.dezgw = API_GW(arl=os.getenv("ARL"))

app.downloads = {}

async def create_aiohttp_session():
    app.aiosession = aiohttp.ClientSession()
    print("Created a AioHttp Session")


app.loop.run_until_complete(create_aiohttp_session())

app.run()