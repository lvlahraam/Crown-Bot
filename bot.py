import logging, os
from deezloader.deezloader import DeeLogin, API, API_GW
import pyrogram

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

app = pyrogram.Client(session_name="robot", bot_token=os.getenv("TOKEN"), plugins=dict(root="plugins")) 

app.dezlog = DeeLogin(arl=os.getenv("ARL"))
app.dezapi = API()
app.dezgw = API_GW(arl=os.getenv("ARL"))

app.downloads = {}

app.run()