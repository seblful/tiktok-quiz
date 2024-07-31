from typing import Tuple, List, Dict

import os
import json
import math
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
        self.quiz = self.quiz_getter.get_random_question(q_type="multiple")

        # Question and answers
        self.question_handler = QuestionHandler(question=self.quiz['question'],
                                                screen_size=screen_size,
                                                font_path=self.font_path,
                                                color=question_color)

        self.answers_handler = AnswersHandler(correct_answer=self.quiz["correct_answer"],
                                              incorrect_answers=self.quiz["incorrect_answers"],
                                              screen_size=screen_size,
                                              font_path=self.font_path,
                                              color=answer_color)

        # Screen
        self.screen_size = screen_size

    def render(self, screen: pygame.Surface, fps: int) -> None:
        self.question_handler.render(screen, fps)
        self.answers_handler.render(screen, fps)

    def update_quiz(self) -> None:
        self.quiz = self.quiz_getter.get_random_question(q_type="multiple")
        self.question_handler.update_question(self.quiz['question'])


class QuestionHandler:
    def __init__(self,
                 question: str,
                 screen_size: Tuple[int, int],
                 font_path: str,
                 color: Tuple[int, int, int]) -> None:
        self.width, self.height = screen_size
        self.font_path = font_path
        self.color = color

        # Text rectangle
        self.width_margin, self.height_margin = 0.05, 0.05
        self.__rect = None

        # Question
        self.question = question

        # Font
        self.setup_font()

    @property
    def rect(self) -> pygame.Rect:
        if self.__rect is None:
            rect_width = self.width - (self.width_margin * 2 * self.width)
            rect_height = 0.3 * self.height
            self.__rect = pygame.Rect(self.width * self.width_margin, self.height * self.height_margin,
                                      rect_width, rect_height)

        return self.__rect

    def setup_font(self) -> None:
        self.font_size = self.calculate_font_size()
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.space_width = self.font.size(' ')[0]

    def calculate_font_size(self) -> int:
        font_size = 1
        words = self.question.split(' ')

        while True:
            font = pygame.font.Font(self.font_path, font_size)
            space_width = font.size(' ')[0]

            x, y = 0, 0
            max_y = 0
            for word in words:
                word_surface = font.render(word, True, self.color)
                word_width, word_height = word_surface.get_size()
                if x + word_width > self.rect.width:
                    x = 0
                    y += word_height
                x += word_width + space_width
                max_y = max(max_y, y + word_height)

            if max_y > self.rect.height or x > self.rect.width:
                return font_size - 1
            font_size += 1

    def render_words(self, screen: pygame.Surface) -> None:
        # Split word
        words = self.question.split(' ')

        # Iterates through words and blit them
        x, y = self.rect.x, self.rect.y
        for word in words:
            word_surface = self.font.render(word, True, self.color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= self.rect.right:
                x = self.rect.x
                y += word_height
            screen.blit(word_surface, (x, y))
            x += word_width + self.space_width

    def render(self, screen: pygame.Surface, fps: int) -> None:
        self.render_words(screen)
        pygame.time.Clock().tick(fps)

    def update_question(self, new_question: str) -> None:
        self.question = new_question
        self.font_size = self.setup_font()


class AnswersHandler:
    def __init__(self,
                 correct_answer: str,
                 incorrect_answers: List[str],
                 screen_size: Tuple[int, int],
                 font_path: str,
                 color: Tuple[int, int]) -> None:
        self.screen_size = screen_size
        self.font_path = font_path
        self.color = color

        # Text rectangles

        # Answers
        self.correct_answer = correct_answer
        self.incorrect_anwers = incorrect_answers

    # Font
    def setup_font(self) -> None:
        pass

    def render_answers(self, screen: pygame.Surface) -> None:
        pass

    def render(self, screen: pygame.Surface, fps: int) -> None:
        self.render_answers(screen)
        pygame.time.Clock().tick(fps)

    def update_question(self, new_question: str) -> None:
        pass
