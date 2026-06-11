import pygame
import sys

from config import *

from game.player import Player
from game.monster import Monster
from game.button import Button
from data.db_manager import DBManager

pygame.init()

pygame.key.set_repeat(
    250,   # 按住300ms后开始重复
    30     # 每40ms重复一次
)

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

boss_warning_timer = 0

db = DBManager()

monsters = []

spawn_timer = 0
spawn_interval = 120

input_text = ""

cursor_timer = 0

cursor_visible = True

running = True

game_state = "menu" #开始菜单
difficulty_mode = "normal"
start_button = Button(
    500,
    320,
    260,
    70,
    "开始游戏",
    font,
    (50, 150, 50),
    (80, 200, 80)
)

exit_button = Button(
    500,
    420,
    260,
    70,
    "退出游戏",
    font,
    (150, 50, 50),
    (220, 80, 80)
)

easy_button = Button(
    470,
    280,
    320,
    70,
    "EASY",
    font,
    (50,150,50),
    (80,220,80)
)

normal_button = Button(
    470,
    380,
    320,
    70,
    "NORMAL",
    font,
    (100,100,100),
    (180,180,180)
)

hard_button = Button(
    470,
    480,
    320,
    70,
    "HARD",
    font,
    (180,50,50),
    (255,80,80)
)

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # ==================
        # 文本输入
        # ==================
        elif event.type == pygame.TEXTINPUT:

            if game_state == "playing":

                cursor_timer += 1

                if cursor_timer >= 30:
                    cursor_timer = 0

                    cursor_visible = not cursor_visible

                text = event.text.lower()

                if text.isalpha():
                    input_text += text

        #这个区分大小写，专门做了优化，采用了大小写不会影响输入，输出都为小写
        # elif event.type == pygame.TEXTINPUT:
        #
        #     if (
        #             game_state == "playing"
        #             and
        #             event.text.isalpha()
        #     ):
        #         input_text += event.text

        # ==================
        # 功能按键
        # ==================

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if game_state == "menu":

                if start_button.is_clicked(event):

                    game_state = "difficulty"

                elif exit_button.is_clicked(event):

                    running = False

            elif game_state == "difficulty":

                if easy_button.is_clicked(event):

                    difficulty_mode = "easy"
                    spawn_interval = 180
                    game_state = "playing"

                elif normal_button.is_clicked(event):

                    difficulty_mode = "normal"
                    spawn_interval = 120
                    game_state = "playing"

                elif hard_button.is_clicked(event):

                    difficulty_mode = "hard"
                    spawn_interval = 80
                    game_state = "playing"

        elif event.type == pygame.KEYDOWN:

            # ==================
            # Game Over 控制
            # ==================

            if player.is_dead():

                if event.key == pygame.K_r:

                    player = Player()

                    monsters.clear()

                    combo = 0

                    input_text = ""

                    spawn_timer = 0

                    boss_spawned_level = 0

                    game_state = "playing"

                elif event.key == pygame.K_ESCAPE:

                    player = Player()

                    monsters.clear()

                    combo = 0

                    input_text = ""

                    spawn_timer = 0

                    boss_spawned_level = 0

                    game_state = "menu"

                continue

            # ==================
            # 菜单
            # ==================
                continue
            # ==================
            # 难度选择
            # ==================

            if game_state == "difficulty":

                if game_state == "difficulty":

                    if easy_button.is_clicked(event):

                        difficulty_mode = "easy"
                        spawn_interval = 180
                        game_state = "playing"

                    elif normal_button.is_clicked(event):

                        difficulty_mode = "normal"
                        spawn_interval = 120
                        game_state = "playing"

                    elif hard_button.is_clicked(event):

                        difficulty_mode = "hard"
                        spawn_interval = 80
                        game_state = "playing"

                    continue

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

    if game_state == "playing":

        if boss_warning_timer > 0:
            boss_warning_timer -= 1

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
                boss_warning_timer = 180

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
    # MENU
    # ==================

    if game_state == "menu":
        screen.fill((20, 20, 20))

        title = big_font.render(
            "小王的英语单词机",
            True,
            WHITE
        )

        title_rect = title.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                180
            )
        )

        start_button.draw(
            screen
        )

        exit_button.draw(
            screen
        )

        screen.blit(
            title,
            title_rect
        )

        pygame.display.update()

        continue

    # ==================
    # DIFFICULTY
    # ==================

    if game_state == "difficulty":
        screen.fill((20, 20, 20))

        title = big_font.render(
            "SELECT DIFFICULTY",
            True,
            WHITE
        )

        easy_button.draw(screen)

        normal_button.draw(screen)

        hard_button.draw(screen)

        screen.blit(title, (250, 180))

        pygame.display.update()

        continue

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

    difficulty_color = WHITE

    if difficulty_mode == "easy":
        difficulty_color = GREEN

    elif difficulty_mode == "hard":
        difficulty_color = RED

    difficulty_text = font.render(
        f"Difficulty: {difficulty_mode.upper()}",
        True,
        difficulty_color
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

    screen.blit(
        difficulty_text,
        (20, 180)
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

    display_text = input_text

    if cursor_visible:
        display_text += "|"

    input_surface = font.render(
        display_text,
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

    if boss_warning_timer > 0:
        warning_text = big_font.render(
            "BOSS INCOMING!",
            True,
            RED
        )

        screen.blit(
            warning_text,
            (
                SCREEN_WIDTH // 2 - 220,
                80
            )
        )

    if player.is_dead():
        game_over = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        restart_text = font.render(
            "Press R To Restart",
            True,
            WHITE
        )

        menu_text = font.render(
            "Press ESC To Menu",
            True,
            WHITE
        )

        screen.blit(
            game_over,
            (
                SCREEN_WIDTH // 2 - 180,
                SCREEN_HEIGHT // 2 - 80
            )
        )

        screen.blit(
            restart_text,
            (
                SCREEN_WIDTH // 2 - 120,
                SCREEN_HEIGHT // 2 + 10
            )
        )

        screen.blit(
            menu_text,
            (
                SCREEN_WIDTH // 2 - 120,
                SCREEN_HEIGHT // 2 + 50
            )
        )

    pygame.display.update()

pygame.quit()
sys.exit()