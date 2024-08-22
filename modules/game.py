from typing import Tuple, List
import os

import pygame

from .quiz import QuizHandler
from .background import Background, Mention, GiftLegend
from .progress_bar import ProgressBar
from .sound import SoundMaker


class GameCreator:
    def __init__(self,
                 json_dir: str,
                 source_dir: str,
                 screen_size: Tuple[int, int] = (360, 640),
                 fps: int = 120) -> None:
        # Paths
        self.json_dir = json_dir
        self.source_dir = source_dir
        self.font_dir = os.path.join(source_dir, "fonts")

        # Init font, mixer
        pygame.font.init()
        pygame.mixer.init()

        # Game modes
        self.game_modes = ("question", "answer")
        self.mode_durations = (30, 10)
        self.mode_index = 0
        self.current_mode = self.game_modes[self.mode_index]
        self.mode_start_time = 0  # Track start time of current mode

        # Video
        self.fps = fps

        # Display and background
        self.screen_size = screen_size
        self.setup_display(source_dir)
        self.background = Background(source_dir=source_dir,
                                     screen_size=screen_size)

        # Text
        self.mention = Mention(screen_size=screen_size,
                               font_dir=os.path.join(source_dir, "fonts"),
                               position="horizontal")

        # Gifts legend
        self.gift_legend = GiftLegend(screen_size=screen_size,
                                      source_dir=source_dir)

        # Counts of gifts
        self.gifts_counter = {k: 0 for k in range(4)}

        # Quiz
        self.quiz_handler = QuizHandler(json_dir=json_dir,
                                        font_dir=os.path.join(
                                            source_dir, "fonts"),
                                        source_dir=source_dir,
                                        screen_size=screen_size)

        # Progress bar
        self.progress_bar = ProgressBar(screen_size=screen_size)

        # Sound
        self.sound_maker = SoundMaker(source_dir=source_dir)

        # Running
        self.running = True

    def setup_display(self, source_dir: str) -> None:
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("LiveQuizMaster")
        icon = pygame.image.load(os.path.join(source_dir, "icon.png"))
        pygame.display.set_icon(icon)

    def check_game_mode(self, ticks: int) -> float:
        elapsed_time = (ticks - self.mode_start_time) / 1000
        if elapsed_time >= self.mode_durations[self.mode_index]:
            # Move to the next mode
            self.mode_index = (self.mode_index + 1) % len(self.game_modes)
            self.current_mode = self.game_modes[self.mode_index]
            self.mode_start_time = ticks  # Reset the start time for the new mode

            # If we've cycled back to the first mode, load the next question
            if self.mode_index == 0:
                self.next_question()

        return elapsed_time

    def is_run_out_question_time(self,
                                 elapsed_time: float,
                                 remain_time_ratio: float = 0.2) -> bool:
        if self.current_mode == "question" and elapsed_time >= (1-remain_time_ratio) * self.mode_durations[0]:
            return True

        return False

    def next_question(self) -> None:
        # Update color of the background
        self.background.update_color()
        # Update question
        self.quiz_handler.update_quiz()
        # Update sounds
        self.sound_maker.update_sounds()
        # Reset gift counter
        self.gifts_counter = {k: 0 for k in range(4)}

    def parse_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Check for key down events
            if event.type == pygame.KEYDOWN:
                # 1 - A
                if event.key == pygame.K_1:
                    self.gifts_counter[0] += 1
                # 2 - B
                if event.key == pygame.K_2:
                    self.gifts_counter[1] += 1
                # 3 - C
                if event.key == pygame.K_3:
                    self.gifts_counter[2] += 1
                # 4 - D
                if event.key == pygame.K_4:
                    self.gifts_counter[3] += 1

    def run(self) -> None:
        # Initialize start time
        self.mode_start_time = pygame.time.get_ticks()
        while self.running:
            self.parse_events()

            # Render background
            self.background.render(self.screen)

            # Mention
            self.mention.render(self.screen)

            # Gifts legend
            self.gift_legend.render(self.screen)

            # Render quiz
            self.quiz_handler.render(self.screen, self.gifts_counter)

            # Get ticks
            ticks = pygame.time.get_ticks()

            # Check game mode
            elapsed_time = self.check_game_mode(ticks)

            # Render progress bar
            if self.current_mode == "question":
                self.progress_bar.render(
                    self.screen, elapsed_time, self.mode_durations[self.mode_index])

            # Show and sound answer
            if self.current_mode == "answer":
                self.quiz_handler.show_answer(self.screen)
                self.sound_maker.make_effect(effect_type="answer")

            # Play ticking
            if self.is_run_out_question_time(elapsed_time):
                self.sound_maker.make_effect(effect_type="tick")

            # Play music
            self.sound_maker.play_music()

            # Flip display
            pygame.display.flip()

            # FPS
            pygame.time.Clock().tick(self.fps)

        # Quit Pygame
        pygame.quit()
