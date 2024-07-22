from typing import Tuple, List

import os

import pygame

from .quiz import QuizHandler
from .background import Background


class GameCreator:
    def __init__(self, json_dir: str,
                 source_dir: str,
                 frame_size: Tuple[int, int] = (360, 640),
                 fps: int = 60) -> None:
        # Paths
        self.json_dir = json_dir
        self.source_dir = source_dir
        self.font_dir = os.path.join(source_dir, "fonts")

        # Game mods
        self.game_modes = ("topic", "question", "answer")
        # (120, 300, 60)  # Duration  of game mods in secondss
        self.mode_durations = (1, 3, 2)
        self.mode_index = 0

        # Questions
        self.quiz_handler = QuizHandler(json_dir)

        # Video
        self.fps = fps

        # Display and background
        self.frame_size = frame_size
        self.setup_display(source_dir)
        self.background = Background(source_dir=source_dir,
                                     screen_size=frame_size)

        # Text
        pygame.font.init()
        self.setup_name()

        # Running
        self.running = True

    def setup_display(self, source_dir: str) -> None:
        self.screen = pygame.display.set_mode(self.frame_size)
        pygame.display.set_caption("LiveQuizMaster")
        icon = pygame.image.load(os.path.join(source_dir, "icon.png"))
        pygame.display.set_icon(icon)

    def setup_name(self):
        name_font = pygame.font.Font(
            os.path.join(self.font_dir, "Zain-Regular.ttf"), 32)
        self.name_surface = name_font.render(
            "@livequizmaster", True, (220, 220, 220))
        self.name_surface = pygame.transform.rotate(self.name_surface, 90)
        self.name_coord = self.name_surface.get_rect(
            center=(self.frame_size[0] * 0.95, self.frame_size[1] * 0.8))

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Render background
            self.background.render(self.screen, self.fps)

            # Name of app
            self.screen.blit(self.name_surface, self.name_coord)

            # Flip display
            pygame.display.flip()

            # Next question
            if pygame.time.get_ticks() % (sum(self.mode_durations) * 1000) < self.fps:
                self.background.update_color()
