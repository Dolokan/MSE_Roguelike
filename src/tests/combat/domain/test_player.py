import pytest

from src.combat.domain.model.Player import Player


@pytest.fixture
def default_player() -> Player:
    """Return a Player instance with default attribute values."""
    return Player(player_id=1)


@pytest.fixture
def armored_player() -> Player:
    """Return a Player instance with armor."""
    return Player(
        player_id=2,
        hp=80,
        max_hp=100,
        armor=5,
        speed=120.0
    )


# ---------------------------------------------------------------------------
# 1. Happy-Path Tests
# ---------------------------------------------------------------------------


def test_player_initialization_with_defaults(default_player: Player) -> None:
    assert default_player.player_id == 1
    assert default_player.hp == 100
    assert default_player.max_hp == 100
    assert default_player.armor == 0
    assert default_player.speed == 100.0


def test_player_initialization_with_custom_values(armored_player: Player) -> None:
    assert armored_player.player_id == 2
    assert armored_player.hp == 80
    assert armored_player.max_hp == 100
    assert armored_player.armor == 5
    assert armored_player.speed == 120.0


def test_take_damage_reduces_hp_without_dying(armored_player: Player) -> None:
    died = armored_player.take_damage(20)

    assert died is False
    assert armored_player.hp == 65  # 80 - max(1, 20 - 5)


def test_heal_damaged_player_up_to_max_hp() -> None:
    player = Player(player_id=1, hp=60, max_hp=100)

    player.heal(25)
    assert player.hp == 85

    player.heal(30)
    assert player.hp == 100


# ---------------------------------------------------------------------------
# 2. Edge Cases (Grenzfälle)
# ---------------------------------------------------------------------------


def test_take_damage_exact_hp_kills_player(default_player: Player) -> None:
    died = default_player.take_damage(100)

    assert died is True
    assert default_player.hp == 0


def test_take_overkill_damage_clamps_hp_to_zero(default_player: Player) -> None:
    died = default_player.take_damage(250)

    assert died is True
    assert default_player.hp == 0


@pytest.mark.parametrize(
    ("armor", "raw_damage", "expected_hp"),
    [
        (10, 5, 99),
        (10, 10, 99),
        (10, 0, 99),
    ],
)
def test_high_armor_clamps_effective_damage_to_minimum_one(
    armor: int, raw_damage: int, expected_hp: int
) -> None:
    player = Player(player_id=1, hp=100, max_hp=100, armor=armor)

    died = player.take_damage(raw_damage)

    assert died is False
    assert player.hp == expected_hp


def test_heal_when_already_at_max_hp_keeps_max_hp(default_player: Player) -> None:
    default_player.heal(50)

    assert default_player.hp == default_player.max_hp


# ---------------------------------------------------------------------------
# 3. Negative Tests (Invalid Inputs & Exception Handling)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "kwargs",
    [
        {"hp": -1},
        {"max_hp": 0},
        {"max_hp": -10},
        {"hp": 101, "max_hp": 100},
        {"armor": -1},
    ],
)
def test_player_initialization_with_invalid_parameters_raises_value_error(
    kwargs: dict,
) -> None:
    with pytest.raises(ValueError):
        Player(player_id=1, **kwargs)


@pytest.mark.parametrize("negative_damage", [-1, -50])
def test_take_damage_negative_raises_value_error(
    default_player: Player, negative_damage: int
) -> None:
    with pytest.raises(ValueError):
        default_player.take_damage(negative_damage)


@pytest.mark.parametrize("invalid_heal_amount", [0, -1, -25])
def test_heal_zero_or_negative_raises_value_error(
    default_player: Player, invalid_heal_amount: int
) -> None:
    with pytest.raises(ValueError):
        default_player.heal(invalid_heal_amount)
