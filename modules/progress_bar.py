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
        self.outer_rect_color = (255, 255, 255)
        self.outer_rect_width = 8

        self.inner_rect_color = (220, 220, 220)

        self.rect_border_radius = 20
        self.__outer_rect = None
        self.__inner_rect = None

    @property
    def outer_rect(self) -> pygame.Rect:
        if self.__outer_rect is None:
            rect_width = self.screen_width - \
                (self.width_margin * 2 * self.screen_width)
            rect_height = self.screen_height * (0.1 - self.height_margin * 2)
            self.__outer_rect = pygame.Rect(self.screen_width * self.width_margin,
                                            self.screen_height * self.height_margin,
                                            rect_width, rect_height)

        return self.__outer_rect

    @property
    def inner_rect(self) -> pygame.Rect:
        if self.__inner_rect is None:
            rect_width = self.outer_rect.width - self.outer_rect_width
            rect_height = self.outer_rect.height - self.outer_rect_width
            self.__inner_rect = pygame.Rect(self.screen_width * self.width_margin + self.outer_rect_width / 2,
                                            self.screen_height * self.height_margin + self.outer_rect_width / 2,
                                            rect_width, rect_height)

        return self.__inner_rect

    def render(self, screen: pygame.Surface) -> None:
        # Draw inner rect
        pygame.draw.rect(screen,
                         self.outer_rect_color,
                         self.outer_rect,
                         width=self.outer_rect_width,
                         border_radius=self.rect_border_radius)

        # Draw outer rect
        pygame.draw.rect(screen,
                         self.inner_rect_color,
                         self.inner_rect,
                         border_radius=self.rect_border_radius)
