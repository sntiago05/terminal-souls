from models import Hero, Enemy
import os


def show_status(hero: Hero, enemy: Enemy):
    print(f"{'='*40} Status {'='*40}")
    print(f"Hero HP: {hero.hp}")
    print(f"Hero potions left: {hero.potions_cuantity}")
    print(f"Enemy HP: {enemy.hp}")
    print(f"{'='*88}\n" )


def player_turn(hero: Hero, enemy: Enemy):
    print("Choose an action:")
    print("1. Attack")
    print("2. Use Potion")
    print("3. Special Attack")

    option = input("choose an option ")
    clear_screen()
    if option == "1":
        hero.attack(enemy)
        return True

    elif option == "2":
        if hero.potions_cuantity > 0:
            hero.use_potion()
            return True
        else:
            print("No potions left.")
            return False

    elif option == "3":
        hero.special(enemy)
        return True

    else:
        print("Invalid option.")
        return False


def enemy_turn(enemy: Enemy, hero: Hero):
    if enemy._is_alive():
        enemy.attack(hero)
    if enemy.hp <= enemy.max_hp * 0.2:
        enemy.auto_heal()


def check_winner(hero: Hero, enemy: Enemy):
    if not hero._is_alive():
        print("You have been defeated...")
        return True

    if not enemy._is_alive():
        print("You defeated the enemy!")
        return True

    return False


def clear_screen():
    input("press enter to continue..")
    os.system("clear")


def main():
    hero = Hero(100, 3)
    enemy = Enemy(120)

    print("Welcome to TERMINAL SOULS")

    while hero._is_alive() and enemy._is_alive():
        show_status(hero, enemy)
        clear_screen()
        valid_action = player_turn(hero, enemy)
        clear_screen()
        if not valid_action:
            continue

        if check_winner(hero, enemy):
            break

        enemy_turn(enemy, hero)
        clear_screen()
        if check_winner(hero, enemy):
            break
    print("Game Over")


if __name__ == "__main__":
    main()
