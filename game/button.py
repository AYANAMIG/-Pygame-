import pygame


class Button:

    def __init__(
            self,
            x,
            y,
            width,
            height,
            text,
            font,
            color,
            hover_color
    ):

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.text = text

        self.font = font

        self.color = color

        self.hover_color = hover_color

    def draw(
            self,
            screen
    ):

        mouse_pos = pygame.mouse.get_pos()

        current_color = self.color

        if self.rect.collidepoint(
                mouse_pos
        ):
            current_color = self.hover_color

        pygame.draw.rect(
            screen,
            current_color,
            self.rect,
            border_radius=8
        )

        text_surface = self.font.render(
            self.text,
            True,
            (255, 255, 255)
        )

        text_rect = text_surface.get_rect(
            center=self.rect.center
        )

        screen.blit(
            text_surface,
            text_rect
        )

    def is_clicked(
            self,
            event
    ):

        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and
            event.button == 1
            and
            self.rect.collidepoint(
                event.pos
            )
        )