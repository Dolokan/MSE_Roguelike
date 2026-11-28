# src/combat/domain/model/Player.py

from dataclasses import dataclass

@dataclass
class Player:
    player_id: int
    name: str = "Player"
    hp: int = 100
    max_hp: int = 100
    armor: int = 0
    speed: float = 100.0
    x: float = 0.0
    y: float = 0.0

    def __post_init__(self) -> None:
        if self.max_hp <= 0:
            raise ValueError("max_hp must be greater than 0.")
        if not (0 <= self.hp <= self.max_hp):
            raise ValueError("hp must be between 0 and max_hp.")
        if self.armor < 0:
            raise ValueError("armor must be non-negative.")
        if len(self.name) == 0:
            raise ValueError("name must not be empty.")
        if len(self.name) > 20:
            raise ValueError("name must not exceed 20 characters.")

    def take_damage(self, raw_damage: int) -> bool:
        if raw_damage < 0:
            raise ValueError("Damage must be non-negative.")
        else:
            effective_damage = max(1, raw_damage - self.armor)
            self.hp = max(0, self.hp - effective_damage)
            return self.hp == 0

    def heal(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Heal amount must be positive.")
        self.hp = min(self.max_hp, self.hp + amount)

    def move(self, dx: float, dy: float, dt: float) -> None:
        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt