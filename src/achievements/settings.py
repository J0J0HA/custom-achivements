import yaml
from pathlib import Path


PROTOCOL_VERSIONS_COMPATIBLE = ["0.3.0"]

BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_PATH = BASE_DIR / ".." / "config" / "config.yml"

with open(CONFIG_PATH, "r", encoding="ascii") as file:
    CONFIG = yaml.load(file, Loader=yaml.Loader)


