from typing import Tuple

import os
import random

import pygame
import pygame.locals

from .quiz import QuizHandler


class GameCreator:
    def __init__(self,
                 json_dir: str,
                 source_dir: str,
                 frame_size: Tuple[int, int] = (
                     360, 640),
                 fps: int = 60,
                 shape_size: int = 50) -> None:

        # Paths
        self.json_dir = json_dir
        self.source_dir = source_dir

        # Game mods
        self.game_mods = ("topic", "question", "answer")
        self.mode_durs = (1, 3, 2)  # (120, 300, 60)  # Duration  of game mods
        self.mode_idx = 0

        # Questions
        self.quiz_handler = QuizHandler(json_dir=json_dir)

        # Video
        self.frame_size = frame_size
        self.fps = fps

        # Screen
        self.screen = pygame.display.set_mode(frame_size)
        self.screen_width = frame_size[0]
        self.screen_height = frame_size[1]

        # Background
        self.bckg_surface = pygame.Surface(frame_size)
        self.bckg_colors = ((255, 190, 11), (251, 86, 7),
                            (255, 0, 110), (131, 56, 236), (58, 134, 255))
        self.bckg_idx = 0
        # Create blank list to store shapes
        self.shapes = []
        self.shape_size = shape_size
        self.create_shapes()

        # Caption and icon
        pygame.display.set_caption("LiveQuizMaster")
        icon = pygame.image.load(os.path.join(source_dir, "icon.png"))
        pygame.display.set_icon(icon)

        self.running = True

    def create_shapes(self, even_rows: int = 5) -> None:
        self.shapes = []
        padding = 20
        available_space_x = self.screen_width - 2 * padding
        available_space_y = self.screen_height - 2 * padding

        # Calculate number of columns (n)
        n = 4  # You can adjust this if needed

        # Calculate intervals
        shape_interval_x = available_space_x / (n - 1)
        shape_interval_y = (available_space_y - even_rows *
                            self.shape_size) / (even_rows - 1)

        for j in range(n):
            rows = even_rows if j % 2 == 0 else even_rows - 1
            for i in range(rows):
                if j % 2 == 0:  # Even columns (0, 2)
                    row_y = padding + i * (self.shape_size + shape_interval_y)
                else:  # Odd columns (1, 3)
                    row_y = padding + (i + 0.5) * \
                        (self.shape_size + shape_interval_y)

                row_x = padding + j * shape_interval_x - self.shape_size  # Start offscreen

                shape = Shape(x=row_x, y=row_y,
                              color=self.bckg_colors[self.bckg_idx % len(
                                  self.bckg_colors)],
                              size=self.shape_size)
                self.shapes.append(shape)

    def run(self):
        while self.running is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Render background
            self.render_background()

    def render_background(self) -> None:
        # Fill background with the color
        self.bckg_surface.fill(
            self.bckg_colors[self.bckg_idx % len(self.bckg_colors)])

        # Move and draw each shape
        for shape in self.shapes:
            shape.move(width=self.screen_width, height=self.screen_height)
            shape.draw(surface=self.bckg_surface)

        # Update the screen
        # Blit the background surface onto the screen
        self.screen.blit(self.bckg_surface, (0, 0))
        pygame.display.flip()
        pygame.time.Clock().tick(self.fps)

        # Change background color after some time
        if pygame.time.get_ticks() % (sum(self.mode_durs) * 1000) < self.fps:  # Change every round
            self.bckg_idx += 1
            self.create_shapes()


class Shape:
    def __init__(self,
                 x: int,
                 y: int,
                 color: Tuple[int, int, int],
                 size: int,
                 speed: float = 3.0
                 ) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.color = self.increase_brightness(color=color, factor=1.2)
        self.size = size

    def increase_brightness(self, color, factor) -> Tuple[int]:
        return tuple(min(255, int(c * factor)) for c in color)

    def move(self, width, height) -> None:
        self.x += self.speed
        if self.x > width:
            self.x = -self.size

    def draw(self, surface) -> None:
        pygame.draw.rect(surface, self.color,
                         (self.x, self.y, self.size, self.size))
