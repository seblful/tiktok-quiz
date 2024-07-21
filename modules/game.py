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
        self.background = Background(source_dir=source_dir,
                                     screen_size=frame_size)
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
