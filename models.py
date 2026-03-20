from __future__ import annotations
from abc import ABC, abstractmethod
import random as rd


class Character(ABC):
    def __init__(self, hp: int) -> None:
        self.hp = hp

    @abstractmethod
    def attack(self, target: Character):
        pass

    @abstractmethod
    def _print_damage(self, damage: int):
        pass

    def _deal_damage(self, start, end, target: Character):
        damage = rd.randint(start, end)

        if rd.random() < 0.10:
            print("¡CRITICAL HIT!")
            damage *= 2

        target.hp -= damage
        return damage

    def _is_alive(self):
        return self.hp > 0


class Hero(Character):
    def __init__(self, hp: int, potions_cuantity) -> None:
        super().__init__(hp)
        self.potions_cuantity = potions_cuantity

    def attack(self, target: Character):
        if target._is_alive():
            print("You attack the enemy!")
            self._print_damage(self._deal_damage(10, 25, target))

    def use_potion(self):
        if self.potions_cuantity > 0:
            self.hp += 20
            self.potions_cuantity -= 1
            print("You used a potion and restored 20 HP!")
            print(f"Potions left: {self.potions_cuantity}")
        else:
            print("No potions left!")

    def special(self, target: Character):
        print("You try a SPECIAL ATTACK...")
        if self._hit_target():
            if target._is_alive():
                print("⚡ Special attack hits!")
                self._print_damage(self._deal_damage(30, 50, target))
        else:
            print("The special attack MISSED!")

    def _hit_target(self):
        return bool(rd.randint(0, 1))

    def _print_damage(self, damage: int):
        print(f"You dealt {damage} damage to the enemy!")


class Enemy(Character):
    def __init__(self, hp: int, max_hp = 120) -> None:
        super().__init__(hp)
        self.max_hp = max_hp

    def attack(self, target: Character):
        if target._is_alive():
            print("Enemy attacks!")
            self._print_damage(self._deal_damage(15, 20, target))

    def _print_damage(self, damage: int):
        print(f"You received {damage} damage!")

    def auto_heal(self):
        self.hp += 20
        print("Enemy regenerates 20 HP!")