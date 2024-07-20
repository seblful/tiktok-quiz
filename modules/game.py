from video import VideoCreator


class GameCreator:
    def __init__(self,
                 topic_duration: int = 120,
                 question_duration: int = 300,
                 answer_duration: int = 60) -> None:

        # Game mods
        self.game_mods = ("start", "topic", "question", "answer")
        self.mode_idx = 0

        # Duration of mods
        self.topic_duration = topic_duration,
        self.question_duration = question_duration,
        self.answer_duration = answer_duration

        # Video
        video_creator = VideoCreator

    def run(self):
        pass
