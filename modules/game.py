from typing import Tuple, List
import os
import pygame
from .quiz import QuizHandler


class Background:
    def __init__(self,
                 screen_size: Tuple[int, int],
                 shape_size: int = 50,
                 padding: int = 20) -> None:
        self.screen_width, self.screen_height = screen_size
        self.surface = pygame.Surface(screen_size)
        self.colors = ((255, 190, 11), (251, 86, 7),
                       (255, 0, 110), (131, 56, 236), (58, 134, 255))
        self.color_index = 0
        self.shapes: List[Shape] = []
        self.shape_size = shape_size
        self.padding = padding
        self.create_shapes()

    def create_shapes(self, even_rows: int = 5, columns: int = 4) -> None:
        self.shapes.clear()
        available_space_x = self.screen_width - 2 * self.padding
        available_space_y = self.screen_height - 2 * self.padding

        shape_interval_x = available_space_x / (columns - 1)
        shape_interval_y = (available_space_y - even_rows *
                            self.shape_size) / (even_rows - 1)

        for col in range(columns):
            rows = even_rows if col % 2 == 0 else even_rows - 1
            for row in range(rows):
                y = self.padding + (row if col % 2 == 0 else row + 0.5) * \
                    (self.shape_size + shape_interval_y)
                x = self.padding + col * shape_interval_x - self.shape_size  # Start offscreen

                shape = Shape(x, y, self.colors[self.color_index % len(
                    self.colors)], self.shape_size)
                self.shapes.append(shape)

    def render(self, screen: pygame.Surface, fps: int) -> None:
        self.surface.fill(self.colors[self.color_index % len(self.colors)])

        for shape in self.shapes:
            shape.move(self.screen_width)
            shape.draw(self.surface)

        screen.blit(self.surface, (0, 0))
        pygame.display.flip()
        pygame.time.Clock().tick(fps)

    def update_color(self) -> None:
        self.color_index += 1

        for shape in self.shapes:
            shape.color = shape.increase_brightness(
                color=self.colors[self.color_index % len(self.colors)])


class Shape:
    def __init__(self,
                 x: int,
                 y: int,
                 color: Tuple[int, int, int],
                 size: int,
                 speed: float = 2.0) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.color = self.increase_brightness(color)
        self.size = size

    @staticmethod
    def increase_brightness(color: Tuple[int, int, int],
                            factor: float = 1.1) -> Tuple[int, int, int]:
        return tuple(min(255, int(c * factor)) for c in color)

    def move(self, width: int) -> None:
        self.x += self.speed
        if self.x > width:
            self.x = -self.size

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color,
                         (self.x, self.y, self.size, self.size))


class GameCreator:
    def __init__(self, json_dir: str,
                 source_dir: str,
                 frame_size: Tuple[int, int] = (360, 640),
                 fps: int = 60) -> None:
        # Paths
        self.json_dir = json_dir
        self.source_dir = source_dir

        # Game mods
        self.game_modes = ("topic", "question", "answer")
        # (120, 300, 60)  # Duration  of game mods in secondss
        self.mode_durations = (1, 3, 2)
        self.mode_index = 0

        # Questions
        self.quiz_handler = QuizHandler(json_dir)

        # Video
        self.fps = fps

        # Screen
        self.screen = pygame.display.set_mode(frame_size)
        self.background = Background(frame_size)
        self.setup_display(source_dir)

        # Running
        self.running = True

    def setup_display(self, source_dir: str) -> None:
        pygame.display.set_caption("LiveQuizMaster")
        icon = pygame.image.load(os.path.join(source_dir, "icon.png"))
        pygame.display.set_icon(icon)

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.background.render(self.screen, self.fps)

            if pygame.time.get_ticks() % (sum(self.mode_durations) * 1000) < self.fps:
                self.background.update_color()
