from pathlib import Path
import tomllib

ROOT_PATH = Path(__file__).parent

_SETTINGS_PATH = ROOT_PATH / "settings.toml"
with _SETTINGS_PATH.open("rb") as f:
    _settings = tomllib.load(f)

GENERAL = _settings["general"]
PLANTS = _settings["plants"]
ZOMBIE = _settings["zombie"]

GAME_TITLE = GENERAL["game_title"]

PLANTS_SCALE = PLANTS["scale"]
PLANTS_DEFAULTS = {"health": PLANTS.get("health")}

PLANTS_SUNFLOWER = {**PLANTS_DEFAULTS, **PLANTS.get("sunflower", {})}
PLANTS_PEASHOOTER = {**PLANTS_DEFAULTS, **PLANTS.get("peashooter", {})}
PLANTS_ICEPEASHOOTER = {**PLANTS_DEFAULTS, **PLANTS.get("icepeashooter", {})}
PLANTS_REPEATER = {**PLANTS_DEFAULTS, **PLANTS.get("repeater", {})}
PLANTS_WALNUT = {**PLANTS_DEFAULTS, **PLANTS.get("walnut", {})}
PLANTS_BLUMERRANG = {**PLANTS_DEFAULTS, **PLANTS.get("blumerrang", {})}

ZOMBIE_SCALE = ZOMBIE["scale"]
ZOMBIE_SPEED = ZOMBIE["speed"]
ZOMBIE_DEFAULTS = {"health": ZOMBIE.get("health")}

ZOMBIE_NORMAL = {**ZOMBIE_DEFAULTS, **ZOMBIE.get("normal", {})}
ZOMBIE_PYLONE = {**ZOMBIE_DEFAULTS, **ZOMBIE.get("pylone", {})}
ZOMBIE_BUCKET = {**ZOMBIE_DEFAULTS, **ZOMBIE.get("bucket", {})}
