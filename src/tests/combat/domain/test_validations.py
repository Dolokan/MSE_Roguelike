# src/tests/combat/domain/test_validations.py

import math

import pytest

from src.combat.domain.validations import (
    validate_player_name,
    validate_rarity_string,
    validate_stat_modifier,
)


# ---------------------------------------------------------------------------
# 1. Happy-Path Tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "name",
    [
        "Hero",
        "Player_1",
        "Knight-99",
        "a1_b2-c3",
        "RogueMaster",
    ],
)
def test_validate_player_name_valid(name: str) -> None:
    assert validate_player_name(name) is True


@pytest.mark.parametrize(
    "value",
    [
        1,
        5,
        0.5,
        1.25,
        2.0,
        100.0,
    ],
)
def test_validate_stat_modifier_valid(value: float) -> None:
    assert validate_stat_modifier(value) is True


@pytest.mark.parametrize(
    ("raw_rarity", "expected"),
    [
        ("COMMON", "COMMON"),
        ("common", "COMMON"),
        ("Rare", "RARE"),
        ("ePiC", "EPIC"),
        ("legendary", "LEGENDARY"),
    ],
)
def test_validate_rarity_string_valid(raw_rarity: str, expected: str) -> None:
    assert validate_rarity_string(raw_rarity) == expected


# ---------------------------------------------------------------------------
# 2. Edge Cases
# ---------------------------------------------------------------------------


def test_validate_player_name_exact_min_length_three() -> None:
    assert validate_player_name("Abc") is True


def test_validate_player_name_exact_max_length_twenty() -> None:
    name_20 = "A" + "b" * 19
    assert len(name_20) == 20
    assert validate_player_name(name_20) is True


@pytest.mark.parametrize(
    "value",
    [
        1e-9,
        0.0001,
        1e-308,
        1e308,
    ],
)
def test_validate_stat_modifier_positive_floating_point_bounds(value: float) -> None:
    assert validate_stat_modifier(value) is True


# ---------------------------------------------------------------------------
# 3. Negative Tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "invalid_name",
    [
        "",
        "Ab",  # too short (2 chars)
        "A" + "b" * 20,  # too long (21 chars)
        "1Player",  # starts with digit
        "_Player",  # starts with underscore
        "-Player",  # starts with hyphen
        "Player One",  # contains space
        "Player!",  # special char
        "Player@home",  # special char
        "Hero\n",  # trailing newline
    ],
)
def test_validate_player_name_invalid(invalid_name: str) -> None:
    assert validate_player_name(invalid_name) is False


@pytest.mark.parametrize(
    "invalid_value",
    [
        0,
        0.0,
        -0.0,
        -0.001,
        -1,
        -100.5,
        math.nan,
        math.inf,
        -math.inf,
        True,
        False,
    ],
)
def test_validate_stat_modifier_invalid(invalid_value: float) -> None:
    assert validate_stat_modifier(invalid_value) is False


@pytest.mark.parametrize(
    "invalid_rarity",
    [
        "",
        "UNCOMMON",
        "MYTHIC",
        "common ",
        " rare",
        "COMMON\n",
        "123",
    ],
)
def test_validate_rarity_string_invalid_raises_value_error(invalid_rarity: str) -> None:
    with pytest.raises(ValueError):
        validate_rarity_string(invalid_rarity)
