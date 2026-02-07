from pathlib import Path
import tomllib



ROOT_PATH = Path(__file__).resolve().parent.parent

_SETTINGS_PATH = ROOT_PATH / "src" / "settings.toml"
with _SETTINGS_PATH.open("rb") as f:
    _settings = tomllib.load(f)

GENERAL = _settings["general"]
PLANTS = _settings["plants"]
ZOMBIE = _settings["zombie"]

GAME_TITLE = GENERAL["game_title"]
WORLD_SCALE = GENERAL["world_scale"]
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

PLANTS_SCALE = PLANTS["scale"]
PLANT_SCALE = PLANTS_SCALE
SUN_SCALE = PLANTS["sun"]["scale"]
PLANT_CARD_SLOTS = int(PLANTS.get("card_max_slots", 7))
PLANT_CARD_ORDER = list(PLANTS.get("card_order", []))
PLANT_CARD_SCALE = float(PLANTS.get("card_scale", 0.7))

PLANTS_DEFAULTS = {k: v for k, v in PLANTS.items() if not isinstance(v, dict)}

def _merge_defaults(defaults, overrides):
    if overrides is None:
        return dict(defaults)
    merged = dict(defaults)
    merged.update(overrides)
    return merged

PLANTS_SUNFLOWER = _merge_defaults(PLANTS_DEFAULTS, PLANTS.get("sunflower"))
PLANTS_PEASHOOTER = _merge_defaults(PLANTS_DEFAULTS, PLANTS.get("peashooter"))
PLANTS_ICEPEASHOOTER = _merge_defaults(PLANTS_DEFAULTS, PLANTS.get("icepeashooter"))
PLANTS_REPEATER = _merge_defaults(PLANTS_DEFAULTS, PLANTS.get("repeater"))
PLANTS_WALNUT = _merge_defaults(PLANTS_DEFAULTS, PLANTS.get("walnut"))
PLANTS_BLUMERRANG = _merge_defaults(PLANTS_DEFAULTS, PLANTS.get("blumerrang"))
PLANTS_POTATOMINE = _merge_defaults(PLANTS_DEFAULTS, PLANTS.get("potatomine"))


def get_plant_config(name: str) -> dict:
    return {
        "sunflower": PLANTS_SUNFLOWER,
        "peashooter": PLANTS_PEASHOOTER,
        "icepeashooter": PLANTS_ICEPEASHOOTER,
        "repeater": PLANTS_REPEATER,
        "walnut": PLANTS_WALNUT,
        "blumerrang": PLANTS_BLUMERRANG,
        "potatomine": PLANTS_POTATOMINE,
    }.get(name, PLANTS_DEFAULTS)

ZOMBIE_SCALE = ZOMBIE["scale"]
ZOMBIE_SPEED = ZOMBIE["speed"]
ZOMBIE_DEFAULTS = {k: v for k, v in ZOMBIE.items() if not isinstance(v, dict)}

ZOMBIE_NORMAL = _merge_defaults(ZOMBIE_DEFAULTS, ZOMBIE.get("normal"))
ZOMBIE_PYLONE = _merge_defaults(ZOMBIE_DEFAULTS, ZOMBIE.get("pylone"))
ZOMBIE_BUCKET = _merge_defaults(ZOMBIE_DEFAULTS, ZOMBIE.get("bucket"))
