import math
import re

PLAYER_NAME_REGEX = r"^[a-zA-Z][a-zA-Z0-9_-]{2,19}$"
RARITY_REGEX = r"^(COMMON|RARE|EPIC|LEGENDARY)$"

_PLAYER_NAME_PATTERN = re.compile(PLAYER_NAME_REGEX)
_RARITY_PATTERN = re.compile(RARITY_REGEX, re.IGNORECASE)

VALID_RARITIES = ("COMMON", "RARE", "EPIC", "LEGENDARY")


def validate_player_name(name: str) -> bool:
    """Validate that a player name is 3-20 chars, starts with a letter, and uses allowed chars."""
    if not isinstance(name, str) or "\n" in name:
        return False
    return bool(_PLAYER_NAME_PATTERN.fullmatch(name))


def validate_stat_modifier(value: float) -> bool:
    """Validate that a stat modifier is a finite, positive, non-zero int or float."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return math.isfinite(value) and value > 0


def validate_rarity_string(rarity: str) -> str:
    """Validate a rarity string (case-insensitive) and return its uppercase form."""
    if not isinstance(rarity, str) or "\n" in rarity:
        raise ValueError(f"Invalid rarity: {rarity!r}. Expected one of {VALID_RARITIES}.")
    if not _RARITY_PATTERN.fullmatch(rarity):
        raise ValueError(f"Invalid rarity: {rarity!r}. Expected one of {VALID_RARITIES}.")
    return rarity.upper()
