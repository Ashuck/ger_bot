import yaml 
from pathlib import Path
from models.settings import Settings
from database import Session

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "config.yaml") as f:
    config = yaml.safe_load(f)


session = Session()
TOKEN = session.query(Settings).filter_by(name="BOT_TOKEN")
session.close()
SRO_TYPES = config["SRO_types"]
TEMPLATES = config["templates"]
CITIES = config["cities"]