import pygame
import sys

from config import *

from game.player import Player
from game.monster import Monster
from data.db_manager import DBManager

pygame.init()

# 开启文本输入
pygame.key.start_text_input()

screen = pygame.display.set_mode(
    (
        SCREEN_WIDTH,
        SCREEN_HEIGHT
    )
)

pygame.display.set_caption(
    GAME_TITLE
)

clock = pygame.time.Clock()

font = pygame.font.SysFont(
    "Microsoft YaHei",
    28
)

big_font = pygame.font.SysFont(
    "Microsoft YaHei",
    60
)

player = Player()

combo = 0

boss_spawned_level = 0

db = DBManager()

monsters = []

spawn_timer = 0
spawn_interval = 120

input_text = ""

running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # ==================
        # 文本输入
        # ==================
        elif event.type == pygame.TEXTINPUT:

            input_text += event.text

        # ==================
        # 功能按键
        # ==================
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_BACKSPACE:

                input_text = input_text[:-1]

            elif event.key == pygame.K_RETURN:

                target = None

                for monster in monsters:

                    if monster.word.lower() == input_text.lower():

                        target = monster
                        break

                if target:

                    dead = target.take_damage()

                    if dead:

                        if target.is_boss:
                            print(
                                f"Boss登场! Level {player.level}"
                            )

                        monsters.remove(target)

                        combo += 1

                        reward = 10 * combo

                        if target.is_boss:

                            reward *= 5

                        player.add_score(
                            reward
                        )

                        player.add_exp(10)

                input_text = ""

    # ==================
    # 游戏逻辑
    # ==================

    if not player.is_dead():

        spawn_timer += 1

        if spawn_timer >= spawn_interval:

            spawn_timer = 0

            word_data = db.get_random_word()

            content = word_data[0]
            hint = word_data[1]
            difficulty = word_data[2]

            difficulty += (
                player.level - 1
            )

            is_boss = False

            if (
                    player.level % 5 == 0
                    and
                    player.level != boss_spawned_level
            ):
                is_boss = True

                boss_spawned_level = player.level

            if is_boss:
                print(
                    f"Boss Spawn! Level {player.level}"
                )

            monsters.append(
                Monster(
                    content,
                    hint,
                    difficulty,
                    is_boss
                )
            )

        for monster in monsters[:]:

            monster.update()

            if monster.reached_base():

                monsters.remove(monster)

                player.take_damage(1)

                combo = 0

    # ==================
    # 绘制
    # ==================

    screen.fill(
        (30, 30, 30)
    )

    hp_text = font.render(
        f"HP: {player.hp}",
        True,
        WHITE
    )

    score_text = font.render(
        f"Score: {player.score}",
        True,
        WHITE
    )

    combo_text = font.render(
        f"Combo: x{combo}",
        True,
        GREEN
    )

    level_text = font.render(
        f"Level: {player.level}",
        True,
        WHITE
    )

    screen.blit(
        hp_text,
        (20, 20)
    )

    screen.blit(
        score_text,
        (20, 60)
    )

    screen.blit(
        combo_text,
        (20, 100)
    )

    screen.blit(
        level_text,
        (20, 140)
    )

    pygame.draw.line(
        screen,
        RED,
        (0, 0),
        (0, SCREEN_HEIGHT),
        5
    )

    for monster in monsters:

        monster.draw(
            screen,
            font
        )

    # ==================
    # 输入框
    # ==================

    pygame.draw.rect(
        screen,
        (60, 60, 60),
        (
            100,
            SCREEN_HEIGHT - 100,
            500,
            50
        )
    )

    input_surface = font.render(
        input_text,
        True,
        WHITE
    )

    screen.blit(
        input_surface,
        (
            110,
            SCREEN_HEIGHT - 90
        )
    )

    # ==================
    # Game Over
    # ==================

    if player.is_dead():

        game_over = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        screen.blit(
            game_over,
            (
                SCREEN_WIDTH // 2 - 180,
                SCREEN_HEIGHT // 2 - 50
            )
        )

    pygame.display.update()

pygame.quit()
sys.exit()