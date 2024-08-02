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
        # Screen, font, color
        self.width, self.height = screen_size
        self.font_path = font_path
        self.color = color

        # Text rectangle
        self.width_margin, self.height_margin = 0.05, 0.1
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

    def draw_rects(self, screen: pygame.Surface):
        # Draw main rect
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

    def setup_font(self) -> None:
        self.font_size = self.calculate_font_size()
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.space_width = self.font.size(' ')[0]

    def calculate_font_size(self) -> int:
        max_font_size = 50  # Start with a large font size
        words = self.question.split(' ')

        for font_size in range(max_font_size, 0, -1):
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

            if max_y <= self.rect.height and x <= self.rect.width:
                return font_size

        return 1

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
        # Draw rect
        self.draw_rects(screen)

        # Render
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
        # Screen, font, color
        self.width, self.height = screen_size
        self.font_path = font_path
        self.color = color

        # Answers
        self.setup_answers(correct_answer, incorrect_answers)

        # Text rectangles
        self.width_margin = 0.05
        self.height_margin = 0.41
        self.inter_w_margin = 0.05
        self.inter_h_margin = 0.05
        self.text_margin = 0.05  # New margin for text
        self.__rect = None
        self.setup_rects()

        # Fonts
        self.setup_fonts()

    def setup_answers(self,
                      correct_answer: str,
                      incorrect_answers: List[str]) -> None:
        self.answers = incorrect_answers.copy()
        correct_idx = random.randint(0, len(incorrect_answers) + 1)
        self.answers.insert(correct_idx, correct_answer)

    @property
    def rect(self) -> pygame.Rect:
        if self.__rect is None:
            rect_width = self.width - (self.width_margin * 2 * self.width)
            rect_height = 0.52 * self.height
            self.__rect = pygame.Rect(self.width * self.width_margin, self.height * self.height_margin,
                                      rect_width, rect_height)

        return self.__rect

    def setup_rects(self) -> None:
        self.answer_rects = []

        # Absolute values of inter margins
        abs_inter_w_margin = self.inter_w_margin * self.rect.width
        abs_inter_h_margin = self.inter_h_margin * self.rect.height

        # Find width and height of answer block
        answer_width = self.rect.width - (2 * abs_inter_w_margin)
        answer_height = (
            self.rect.height - ((len(self.answers) + 1)) * abs_inter_h_margin) / len(self.answers)

        # Create answer rectangles and add it to all rectangles
        abs_h_margin = self.height * self.height_margin + abs_inter_h_margin

        for i in range(len(self.answers)):
            answer_rect = pygame.Rect(self.width * self.width_margin + abs_inter_w_margin, abs_h_margin,
                                      answer_width, answer_height)
            self.answer_rects.append(answer_rect)

            abs_h_margin += answer_height + abs_inter_h_margin

    def draw_rects(self, screen: pygame.Surface) -> None:
        # Draw main rect
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        # Draw answer rects
        for rect in self.answer_rects:
            pygame.draw.rect(screen, (255, 255, 255, ),
                             rect, 0, border_radius=30)

    def setup_fonts(self) -> None:
        # Create empty list to store fonts
        self.fonts = []

        # Iterate through answers and rects
        for i in range(len(self.answers)):
            answer = self.answers[i]
            rect = self.answer_rects[i]

            # Find font size and create fonts
            font_size = self.calculate_font_size(answer, rect)
            font = pygame.font.Font(self.font_path, font_size)

            # Append font to the list
            self.fonts.append(font)
            # self.space_width = self.font.size(' ')[0]

    def calculate_font_size(self, answer: str, rect: pygame.Rect) -> int:
        max_font_size = 50  # Start with a large font size
        words = answer.split(' ')

        for font_size in range(max_font_size, 0, -1):
            font = pygame.font.Font(self.font_path, font_size)
            space_width = font.size(' ')[0]

            x, y = self.text_margin * rect.width, self.text_margin * rect.height
            max_y = 0
            for word in words:
                word_surface = font.render(word, True, self.color)
                word_width, word_height = word_surface.get_size()
                if x + word_width > rect.width - (2 * self.text_margin * rect.width):
                    x = self.text_margin * rect.width
                    y += word_height
                x += word_width + space_width
                max_y = max(max_y, y + word_height)

            if max_y <= rect.height - (2 * self.text_margin * rect.height) and x <= rect.width - (2 * self.text_margin * rect.width):
                return font_size

        return 1

    def render_words(self, screen: pygame.Surface) -> None:
        for i in range(len(self.answers)):
            answer = self.answers[i]
            rect = self.answer_rects[i]

            # Split word
            words = answer.split(' ')

            # Retrieve space width
            space_width = self.fonts[i].size(' ')[0]

            # Calculate the total height of the text
            total_height = 0
            for word in words:
                word_surface = self.fonts[i].render(word, True, self.color)
                word_width, word_height = word_surface.get_size()
                total_height += word_height

            # Calculate the y offset to center the text
            y_offset = (rect.height - total_height) / 2

            # Iterates through words and blit them
            x, y = rect.x + self.text_margin * rect.width, rect.y + \
                y_offset + self.text_margin * rect.height
            for word in words:
                word_surface = self.fonts[i].render(word, True, self.color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= rect.right - self.text_margin * rect.width:
                    x = rect.x + self.text_margin * rect.width
                    y += word_height
                screen.blit(word_surface, (x, y))
                x += word_width + space_width

    def render(self, screen: pygame.Surface, fps: int) -> None:
        # Draw rects
        self.draw_rects(screen)

        # Render
        self.render_words(screen)
        pygame.time.Clock().tick(fps)

    def update_question(self, new_question: str) -> None:
        pass
