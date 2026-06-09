import pygame
import random


class Monster:

    def __init__(
            self,
            word,
            hint,
            difficulty,
            is_boss=False
    ):

        self.word = word
        self.hint = hint
        self.difficulty = difficulty

        self.is_boss = is_boss

        if is_boss:

            self.hp = 3

            self.width = 260
            self.height = 100

        else:

            self.hp = 1

            self.width = 180
            self.height = 70

        self.x = 1300

        self.y = random.randint(
            120,
            550
        )

        self.speed = 2 + difficulty

    def update(self):

        self.x -= self.speed

    def take_damage(self):

        self.hp -= 1

        return self.hp <= 0

    def draw(
            self,
            screen,
            font
    ):

        hint_text = font.render(
            self.hint,
            True,
            (255, 255, 0)
        )

        screen.blit(
            hint_text,
            (
                self.x,
                self.y - 30
            )
        )

        if self.is_boss:

            color = (255, 120, 0)

        else:

            color = (200, 50, 50)

        pygame.draw.rect(
            screen,
            color,
            (
                self.x,
                self.y,
                self.width,
                self.height
            ),
            border_radius=8
        )

        word_text = font.render(
            self.word,
            True,
            (255, 255, 255)
        )

        screen.blit(
            word_text,
            (
                self.x + 10,
                self.y + 20
            )
        )

        # 血量显示

        if self.hp > 1:

            hp_text = font.render(
                str(self.hp),
                True,
                (255, 255, 255)
            )

            screen.blit(
                hp_text,
                (
                    self.x + self.width - 30,
                    self.y + 10
                )
            )

    def reached_base(self):

        return self.x <= 0