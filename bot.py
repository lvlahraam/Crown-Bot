import logging, os, requests, shutil
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

def image(name, url):
    response = requests.get(url, stream=True)
    with open(F"{name}.jpeg", 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
app.image = image

app.run()