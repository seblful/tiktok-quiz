import pygame


class ProgressBar:
    def __init__(self,
                 screen_size) -> None:
        # Screen
        self.screen_width, self.screen_height = screen_size

        # Bar properties
        self.width_margin = 0.05
        self.height_margin = 0.02

        # Bar filling colors
        self.start_color = (0, 255, 0)
        self.end_color = (255, 0, 0)

        # Rects
        self.__outer_rect = None
        self.__inner_rect = None

    @property
    def outer_rect(self) -> pygame.Rect:
        if self.__outer_rect is None:
            rect_width = self.screen_width - \
                (self.width_margin * 2 * self.screen_width)
            rect_height = self.screen_height * (0.1 - self.height_margin * 2)
            self.__outer_rect = pygame.Rect(self.screen_width * self.width_margin, self.screen_height * self.height_margin,
                                            rect_width, rect_height)

        return self.__outer_rect

    def render(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, (255, 255, 255),
                         self.outer_rect, width=4, border_radius=20)
