from typing import Tuple, List

import os

import pygame

from .quiz import QuizHandler
from .background import Background, Mention
from .progress_bar import ProgressBar


class GameCreator:
    def __init__(self,
                 json_dir: str,
                 source_dir: str,
                 screen_size: Tuple[int, int] = (360, 640),
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

        # Video
        self.fps = fps

        # Display and background
        self.screen_size = screen_size
        self.setup_display(source_dir)
        self.background = Background(source_dir=source_dir,
                                     screen_size=screen_size)

        # Text
        pygame.font.init()
        self.mention = Mention(screen_size=screen_size,
                               font_dir=os.path.join(source_dir, "fonts"),
                               position="horizontal")

        # Quiz
        self.quiz_handler = QuizHandler(json_dir=json_dir,
                                        font_dir=os.path.join(
                                            source_dir, "fonts"),
                                        screen_size=screen_size)

        # Progress bar
        self.progress_bar = ProgressBar(screen_size=screen_size)

        # Running
        self.running = True

    def setup_display(self, source_dir: str) -> None:
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("LiveQuizMaster")
        icon = pygame.image.load(os.path.join(source_dir, "icon.png"))
        pygame.display.set_icon(icon)

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Render background
            self.background.render(self.screen)

            # Mention
            self.mention.render(self.screen)

            # Render quiz
            self.quiz_handler.render(self.screen)

            # Flip display
            pygame.display.flip()

            # Render progress bar
            self.progress_bar.render(self.screen)

            # FPS
            pygame.time.Clock().tick(self.fps)

            # Next question
            if pygame.time.get_ticks() % (sum(self.mode_durations) * 1000) < self.fps:
                # Update color of the background
                self.background.update_color()
                # Update question
                self.quiz_handler.update_quiz()

        # Quit Pygame
        pygame.quit()
