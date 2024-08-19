from typing import Tuple, List, Dict

import os
import json
import random

import pygame

from .sound import VoiceMaker


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
                 source_dir: str,
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

        # Voice
        self.voice_maker = VoiceMaker(source_dir=source_dir)

        # Screen
        self.screen_size = screen_size

    def render(self, screen: pygame.Surface) -> None:
        self.question_handler.render(screen)
        self.answers_handler.render(screen)
        self.voice_maker.make_voice(
            "q_and_a", self.question_handler.question, self.answers_handler.answers)

    def show_answer(self, screen: pygame.Surface) -> None:
        self.answers_handler.show_answer(screen)
        self.voice_maker.make_voice(
            "right_answer", self.answers_handler.answers[self.answers_handler.correct_idx])

    def update_quiz(self) -> None:
        self.quiz = self.quiz_getter.get_random_question(q_type="multiple")
        self.question_handler.update_question(self.quiz['question'])
        self.answers_handler.update_answers(
            self.quiz["correct_answer"], self.quiz["incorrect_answers"])
        self.voice_maker.update_voices()


class QuestionHandler:
    def __init__(self,
                 question: str,
                 screen_size: Tuple[int, int],
                 font_path: str,
                 color: Tuple[int, int, int]) -> None:
        """
        Initialize the QuestionHandler with the given question, screen size, font, and color.

        :param question: The question string to display
        :param screen_size: Tuple containing screen width and height
        :param font_path: Path to the font file
        :param color: Tuple containing the RGB color values
        """
        self.width, self.height = screen_size
        self.font_path = font_path
        self.color = color

        self.width_margin = 0.07
        self.height_margin = 0.1
        self.__rect = None

        self.question = question

        self.setup_font()

    @property
    def rect(self) -> pygame.Rect:
        if self.__rect is None:
            rect_width = self.width - (self.width_margin * 2 * self.width)
            rect_height = 0.3 * self.height
            self.__rect = pygame.Rect(self.width * self.width_margin, self.height * self.height_margin,
                                      rect_width, rect_height)
        return self.__rect

    def draw_rect(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

    def setup_font(self) -> None:
        self.font_size = self.calculate_font_size()
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.space_width = self.font.size(' ')[0]

    def calculate_font_size(self) -> int:
        max_font_size = 50
        words = self.question.split(' ')

        for font_size in range(max_font_size, 0, -1):
            font = pygame.font.Font(self.font_path, font_size)
            space_width = font.size(' ')[0]

            if self.does_text_fit(font, words, space_width):
                return font_size

        return 1

    def does_text_fit(self, font: pygame.font.Font, words: list, space_width: int) -> bool:
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

        return max_y <= self.rect.height and x <= self.rect.width

    def render_words(self, screen: pygame.Surface) -> None:
        words = self.question.split(' ')

        x, y = self.rect.x, self.rect.y
        for word in words:
            word_surface = self.font.render(word, True, self.color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= self.rect.right:
                x = self.rect.x
                y += word_height
            screen.blit(word_surface, (x, y))
            x += word_width + self.space_width

    def render(self, screen: pygame.Surface) -> None:
        # self.draw_rect(screen)
        self.render_words(screen)

    def update_question(self, new_question: str) -> None:
        self.question = new_question
        self.setup_font()


class AnswersHandler:
    def __init__(self,
                 correct_answer: str,
                 incorrect_answers: List[str],
                 screen_size: Tuple[int, int],
                 font_path: str,
                 color: Tuple[int, int]) -> None:
        """
        Initialize the AnswersHandler with given answers, screen size, font, and color.

        :param correct_answer: The correct answer string
        :param incorrect_answers: A list of incorrect answer strings
        :param screen_size: Tuple containing screen width and height
        :param font_path: Path to the font file
        :param color: Tuple containing the RGB color values
        """
        self.width, self.height = screen_size
        self.font_path = font_path
        self.color = color

        self.width_margin = 0.09
        self.height_margin = 0.41
        self.inter_w_margin = 0.05
        self.inter_h_margin = 0.05
        self.text_margin = 0.13
        self.__rect = None

        self.letter_size = 50
        self.letter_color = (255, 255, 255)
        self.letters = ['A', 'B', 'C', 'D']

        self.update_answers(correct_answer, incorrect_answers)

    def setup_answers(self, correct_answer: str, incorrect_answers: List[str]) -> None:
        self.answers = incorrect_answers.copy()
        self.correct_idx = random.randint(0, len(incorrect_answers))
        self.answers.insert(self.correct_idx, correct_answer)

    @property
    def rect(self) -> pygame.Rect:
        if self.__rect is None:
            rect_width = self.width - (self.width_margin * self.width)
            rect_height = 0.52 * self.height
            self.__rect = pygame.Rect(self.width * self.width_margin, self.height * self.height_margin,
                                      rect_width, rect_height)
        return self.__rect

    def setup_rects(self) -> None:
        self.answer_rects = []
        abs_inter_w_margin = self.inter_w_margin * self.rect.width
        abs_inter_h_margin = self.inter_h_margin * self.rect.height

        answer_width = self.rect.width - (2 * abs_inter_w_margin)
        answer_height = (self.rect.height - ((len(self.answers) + 1)
                         * abs_inter_h_margin)) / len(self.answers)

        abs_h_margin = self.height * self.height_margin + abs_inter_h_margin

        for _ in self.answers:
            answer_rect = pygame.Rect(self.width * self.width_margin + abs_inter_w_margin, abs_h_margin,
                                      answer_width, answer_height)
            self.answer_rects.append(answer_rect)
            abs_h_margin += answer_height + abs_inter_h_margin

    def draw_answers(self, screen: pygame.Surface,
                     i: int,
                     color=(255, 0, 40),
                     draw_rectangle=True,
                     factor=1):
        # Answers rect
        if draw_rectangle is True:
            pygame.draw.rect(screen, (255, 255, 255),
                             self.answer_rects[i], 0,
                             border_top_right_radius=25, border_bottom_right_radius=25)

        # Circless
        pygame.draw.circle(screen, color,
                           self.answer_rects[i].midleft, self.answer_rects[i].height / 2 * factor)
        # Letter
        letter_font = pygame.font.Font(
            self.font_path, int(self.letter_size * factor))
        letter = letter_font.render(
            self.letters[i], True, self.letter_color)
        letter_rect = letter.get_rect(center=self.answer_rects[i].midleft)
        screen.blit(letter, letter_rect)

    def draw(self, screen: pygame.Surface) -> None:
        # # Draw main rect
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        # Draw answers rect and circles
        for i in range(len(self.answers)):

            self.draw_answers(screen, i)

    def setup_fonts(self) -> None:
        self.fonts = [self.create_font(answer, rect) for answer, rect in zip(
            self.answers, self.answer_rects)]

    def create_font(self, answer: str, rect: pygame.Rect) -> pygame.font.Font:
        max_font_size = 50
        words = answer.split(' ')

        for font_size in range(max_font_size, 0, -1):
            font = pygame.font.Font(self.font_path, font_size)
            space_width = font.size(' ')[0]
            x = self.text_margin * rect.width
            max_y = 0
            y = 0

            for word in words:
                word_surface = font.render(word, True, self.color)
                word_width, word_height = word_surface.get_size()
                if x + word_width > rect.width:
                    x = self.text_margin * rect.width
                    y += word_height
                x += word_width + space_width
                max_y = max(max_y, y + word_height)

            if max_y <= rect.height:
                return font

        return pygame.font.Font(self.font_path, 1)

    def render_words(self, screen: pygame.Surface) -> None:
        for answer, rect, font in zip(self.answers, self.answer_rects, self.fonts):
            words = answer.split(' ')
            space_width = font.size(' ')[0]

            total_height = self.calculate_total_height(words, font, rect.width)
            y_offset = (rect.height - total_height) / 2

            x = rect.x + self.text_margin * rect.width
            y = rect.y + y_offset
            line_width = 0
            current_line_height = 0

            for word in words:
                word_surface = font.render(word, True, self.color)
                word_width, word_height = word_surface.get_size()

                if line_width + word_width >= rect.width - self.text_margin * rect.width:
                    x = rect.x + self.text_margin * rect.width
                    y += current_line_height
                    current_line_height = word_height
                    line_width = 0

                screen.blit(word_surface, (x, y))
                x += word_width + space_width
                line_width += word_width + space_width
                current_line_height = max(current_line_height, word_height)

    def calculate_total_height(self, words: List[str], font: pygame.font.Font, rect_width: int) -> int:
        space_width = font.size(' ')[0]
        line_width = 0
        max_line_height = 0
        total_height = 0

        for word in words:
            word_width, word_height = font.size(word)
            if line_width + word_width >= rect_width - self.text_margin * rect_width:
                total_height += max_line_height
                line_width = 0
                max_line_height = word_height

            line_width += word_width + space_width
            max_line_height = max(max_line_height, word_height)

        total_height += max_line_height
        return total_height

    def render(self, screen: pygame.Surface) -> None:
        self.draw(screen)
        self.render_words(screen)

    def show_answer(self, screen: pygame.Surface):
        self.draw_answers(screen, self.correct_idx, color=(
            0, 255, 40), draw_rectangle=False, factor=1.2)

    def update_answers(self, new_correct_answer: str, new_incorrect_answers: List[str]) -> None:
        self.setup_answers(new_correct_answer, new_incorrect_answers)
        self.setup_rects()
        self.setup_fonts()
