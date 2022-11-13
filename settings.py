import yaml
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "config.yaml") as f:
    config = yaml.safe_load(f)

TOKEN = config["bot"]["token"]
SRO_TYPES = config["SRO_types"]
TEMPLATES = config["templates"]
CITIES = config["cities"]