from typing import Tuple, List, Dict

import os
import json
import random

import pygame


class QuizGetter:
    def __init__(self,
                 json_dir: str) -> None:
        # Paths
        self.json_dir = json_dir
        self.mult_q_path = os.path.join(
            json_dir, "trivia_questions_multiple.json")
        self.bool_q_path = os.path.join(
            json_dir, "trivia_questions_boolean.json")

        # JSONs
        self.mult_q_dict = self.load_json(json_path=self.mult_q_path)
        self.bool_q_dict = self.load_json(json_path=self.bool_q_path)

        # Length of the dicts
        self.mult_q_len = len(self.mult_q_dict)
        self.bool_q_len = len(self.bool_q_dict)

        # Indexes that was used before
        self.mult_idxs: List[int] = []
        self.bool_idxs: List[int] = []

    def load_json(self, json_path: str) -> List[Dict[str, str]]:
        with open(json_path, 'r') as file:
            data = json.load(file)

        return data

    def get_random_question(self, q_type: str) -> Dict:
        assert q_type in [
            "multiple", "boolean"], "Type of the question must be one of ['multiple', 'boolean']."

        # Choose dict and idxs
        q_dict = self.mult_q_dict if q_type == "multiple" else self.bool_q_dict
        used_idxs = self.mult_idxs if q_type == "multiple" else self.bool_idxs

        # Choose random index from free indexes
        free_idxs = [i for i in range(len(q_dict)) if i not in used_idxs]
        rand_idx = random.choice(free_idxs)
        used_idxs.append(rand_idx)

        return q_dict[rand_idx]


class QuizHandler:
    def __init__(self,
                 json_dir: str,
                 font_dir: str,
                 screen_size: Tuple[int, int],
                 question_color: Tuple[int, int, int] = (255, 255, 255),
                 answer_color: Tuple[int, int, int] = (0, 0, 0),
                 font_name: str = "Rubik-Medium.ttf") -> None:

        # Paths
        self.font_path = os.path.join(font_dir, font_name)

        # Guiz getter
        self.quiz_getter = QuizGetter(json_dir=json_dir)

        # Question and answers
        self.question_handler = QuestionHandler(screen_size=screen_size,
                                                font_path=self.font_path,
                                                color=question_color)

        self.answers_handler = AnswersHandler(screen_size=screen_size,
                                              font_path=self.font_path,
                                              color=answer_color)

        # Screen
        self.screen_size = screen_size

    def render(self, screen: pygame.Surface, fps: int) -> None:
        self.question_handler.render(screen, fps)
        self.answers_handler.render(screen, fps)


class QuestionHandler:
    def __init__(self,
                 screen_size: Tuple[int, int],
                 font_path: str,
                 color: Tuple[int, int]) -> None:
        self.width, self.height = screen_size
        self.font_path = font_path
        self.color = color

        # Setup surface
        self.setup_surface(
            text='In Kingdom Hearts which of the following people can NOT wield a keyblade?')

    def render_text(surface, text, pos, font, color=pygame.Color('black'), max_width=None):
        words = text.split(' ')
        space_width = font.size(' ')[0]
        x, y = pos

        if max_width is None:
            max_width = surface.get_width() - x

        for word in words:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset x
                y += word_height  # Move to next line
            surface.blit(word_surface, (x, y))
            x += word_width + space_width

        return (x, y)

    def setup_surface(self, text: str) -> None:
        self.font = pygame.font.Font(self.font_path, 30)
        self.surface = self.font.render(text, True, self.color)
        self.rect = self.surface.get_rect(topleft=(0.1 * self.width, 0.1 * self.height),
                                          size=(0.9 * self.width, 0.3 * self.height))

    def render(self, screen: pygame.Surface, fps: int) -> None:
        screen.blit(self.surface, self.rect)
        pygame.time.Clock().tick(fps)


class AnswersHandler:
    def __init__(self,
                 screen_size: Tuple[int, int],
                 font_path: str,
                 color: Tuple[int, int]) -> None:
        self.screen_isze = screen_size
        self.font_path = font_path
        self.color = color

    def setup_surface(self, text: str) -> None:
        pass

    def render(self, screen: pygame.Surface, fps: int) -> None:
        pass
