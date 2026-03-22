# Terminal Souls — Project Documentation

## Overview

**Terminal Souls** is a turn-based RPG combat game played entirely in the terminal. The player controls a Hero who must defeat an Enemy by choosing actions each turn: attacking, using potions, or launching a special attack. The Enemy fights back automatically, and the game ends when one side runs out of HP.

---

## Project Structure

```
├── main.py       # Game loop, UI helpers, and turn logic
└── models.py     # Character class hierarchy (Hero, Enemy)
```

---

## `models.py` — Character Classes

### `Character` (Abstract Base Class)

The base class for all characters in the game. Defines shared behavior and enforces a common interface via abstract methods.

**Constructor**

```python
Character(hp: int)
```

| Parameter | Type  | Description                    |
|-----------|-------|--------------------------------|
| `hp`      | `int` | Starting hit points            |

**Methods**

| Method | Description |
|--------|-------------|
| `attack(target)` | *(Abstract)* Defines how the character attacks a target. |
| `_print_damage(damage)` | *(Abstract)* Prints damage output in a character-specific format. |
| `_deal_damage(start, end, target)` | Rolls a random damage value between `start` and `end`, applies it to the target's HP. Has a 10% chance to trigger a **critical hit** that doubles the damage. Returns the damage dealt. |
| `_is_alive()` | Returns `True` if HP is greater than 0. |

---

### `Hero(Character)`

Represents the player-controlled character.

**Constructor**

```python
Hero(hp: int, potions_cuantity: int)
```

| Parameter          | Type  | Description                        |
|--------------------|-------|------------------------------------|
| `hp`               | `int` | Starting hit points                |
| `potions_cuantity` | `int` | Number of healing potions available|

**Methods**

| Method | Description |
|--------|-------------|
| `attack(target)` | Deals 10–25 damage to the target if it is alive. |
| `use_potion()` | Restores 20 HP and consumes one potion. Prints a warning if no potions remain. |
| `special(target)` | Attempts a special attack (50% hit chance). On hit, deals 30–50 damage. |
| `_hit_target()` | Returns `True` or `False` randomly (50/50) to determine if the special attack connects. |
| `_print_damage(damage)` | Prints: `"You dealt X damage to the enemy!"` |

---

### `Enemy(Character)`

Represents the AI-controlled opponent.

**Constructor**

```python
Enemy(hp: int, max_hp: int = 120)
```

| Parameter | Type  | Description                              |
|-----------|-------|------------------------------------------|
| `hp`      | `int` | Starting hit points                      |
| `max_hp`  | `int` | Maximum HP, used to trigger auto-healing |

**Methods**

| Method | Description |
|--------|-------------|
| `attack(target)` | Deals 15–20 damage to the target if it is alive. |
| `auto_heal()` | Restores 20 HP. Triggered automatically when HP falls below 20% of `max_hp`. |
| `_print_damage(damage)` | Prints: `"You received X damage!"` |

---

## `main.py` — Game Logic

### `show_status(hero, enemy)`

Displays the current HP and potion count for both the Hero and the Enemy in a formatted status bar.

```
======================================== Status ========================================
Hero HP: 80
Hero potions left: 2
Enemy HP: 95
========================================================================================
```

---

### `player_turn(hero, enemy) → bool`

Prompts the player to choose an action:

| Option | Action | Returns |
|--------|--------|---------|
| `1` | Normal attack | `True` |
| `2` | Use potion (if available) | `True` / `False` if no potions |
| `3` | Special attack | `True` |
| Other | Invalid input message | `False` |

Returns `True` if the turn was valid and consumed, `False` otherwise (the game loop will `continue` and not advance the enemy turn).

---

### `enemy_turn(enemy, hero)`

Executes the enemy's turn automatically:
1. Attacks the Hero if still alive.
2. Checks if HP has dropped below 20% of `max_hp` — if so, triggers `auto_heal()`.

---

### `check_winner(hero, enemy) → bool`

Checks if either character has been defeated:
- Hero dead → prints `"You have been defeated..."` → returns `True`
- Enemy dead → prints `"You defeated the enemy!"` → returns `True`
- Both alive → returns `False`

---

### `clear_screen()`

Pauses the game by waiting for the player to press **Enter**, then clears the terminal using `os.system("clear")`.

---

### `main()`

The main game loop:

1. Creates a `Hero` (100 HP, 3 potions) and an `Enemy` (120 HP).
2. Prints a welcome message.
3. Loops while both characters are alive:
   - Shows the status panel.
   - Clears the screen.
   - Runs the player's turn; skips the enemy turn if the action was invalid.
   - Checks for a winner.
   - Runs the enemy's turn.
   - Checks for a winner again.
4. Prints `"Game Over"` when the loop ends.

---

## Game Flow Diagram

```
Start
  │
  ▼
Show Status
  │
  ▼
Player chooses action ──► Invalid? ──► Back to top
  │
  ▼
Apply action (attack / potion / special)
  │
  ▼
Check winner ──► Enemy dead? ──► "You won!" ──► End
  │
  ▼
Enemy attacks Hero
  │
  ▼
Enemy HP < 20%? ──► Auto-heal
  │
  ▼
Check winner ──► Hero dead? ──► "You lost!" ──► End
  │
  ▼
Back to top
```

---

## Combat Mechanics Summary

| Mechanic         | Details                                              |
|------------------|------------------------------------------------------|
| Hero normal attack | 10–25 damage                                      |
| Hero special attack | 30–50 damage, 50% hit chance                    |
| Enemy attack      | 15–20 damage per turn                               |
| Critical hit      | 10% chance on any `_deal_damage` call, doubles damage |
| Potion            | Restores 20 HP; Hero starts with 3                  |
| Enemy auto-heal   | Restores 20 HP when HP ≤ 20% of `max_hp`           |

---

## Notes

- `potions_cuantity` is a typo carried over from the source code; the intended spelling is `potions_quantity`.
- `os.system("clear")` works on Unix/macOS. For Windows compatibility, replace with `os.system("cls")`.
- The `Enemy.auto_heal()` method has no usage cap — the enemy will heal every turn it remains at low HP.