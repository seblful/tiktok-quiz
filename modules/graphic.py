from typing import Tuple


class GraphicCreator:
    def __init__(self,
                 frame_size: Tuple[int, int] = (1080, 1920),
                 topic_duration: int = 120,
                 question_duration: int = 300,
                 answer_duration: int = 60,
                 ):
        self.frame_size = frame_size

        self.topic_duration = topic_duration,
        self.question_duration = question_duration,
        self.answer_duration = answer_duration

    def render(self):
        pass
