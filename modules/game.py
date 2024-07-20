from typing import Tuple

from quiz import QuizHandler


class GameCreator:
    def __init__(self,
                 json_dir: str,
                 frame_size: Tuple[int, int] = (1080, 1920),
                 fps: int = 60) -> None:

        # Game mods
        self.game_mods = ("start", "topic", "question", "answer")
        self.mode_durs = (60, 120, 300, 60)  # Duration  of game mods
        self.mode_idx = 0

        # Questions
        self.quiz_handler = QuizHandler(json_dir=json_dir)

        # Video
        self.frame_size = frame_size
        self.fps = fps

    def run(self):
        pass
