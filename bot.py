from pyrogram import Client
from deezloader import deezloader
import logging, os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Client(session_name="crownmusicbot", bot_token=os.getenv("TOKEN"), api_id=os.getenv("API_ID"), api_hash=os.getenv("API_HASH"), plugins=dict(root="plugins")) 

app.dezlog = deezloader.DeeLogin(arl=os.getenv("ARL"))
app.dezapi = deezloader.API()

app.downloads = {}

app.run()
