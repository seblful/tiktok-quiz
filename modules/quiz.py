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
                 source_dir: str,
                 font_dir: str,
                 screen_size: Tuple[int, int],
                 question_color: Tuple[int, int, int] = (255, 255, 255),
                 answer_color: Tuple[int, int, int] = (0, 0, 0),
                 font_name: str = "Rubik-Medium.ttf",
                 question_font_size: str = 50,
                 answer_font_size: str = 36) -> None:

        # Paths
        self.source_dir = source_dir
        self.font_dir = font_dir
        self.font_path = os.path.join(font_dir, font_name)

        # Guiz getter
        self.quiz_getter = QuizGetter(json_dir=json_dir)

        # Screen
        self.screen_size = screen_size

        # Fonts
        self.question_font = pygame.font.Font(
            self.font_path, question_font_size)
        self.answer_font = pygame.font.Font(self.font_path, answer_font_size)

        # Colors
        self.question_color = question_color
        self.answer_color = answer_color
