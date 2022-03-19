import logging, os, requests, shutil
from deezloader import deezloader
import pyrogram

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

app = pyrogram.Client(session_name="crownmusicbot", bot_token=os.getenv("TOKEN"), api_id=os.getenv("API_ID"), api_hash=os.getenv("API_HASH"), plugins=dict(root="plugins")) 

app.dezlog = deezloader.DeeLogin(arl=os.getenv("ARL"))
app.dezapi = deezloader.API()
app.dezgw = deezloader.API_GW(arl=os.getenv("ARL"))

app.downloads = {}

async def progress(message:pyrogram.types.Message, current:int, total:int):
    await message.edit_text(F"{current * 100 / total:.1f}%")
app.progress = progress

app.run()