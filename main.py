import os

from modules.quiz import OpentdbAPIHandler, QuizHandler

HOME = os.getcwd()
DATA_DIR = os.path.join(HOME, 'data')


def main() -> None:
    api_handler = OpentdbAPIHandler(json_dir=DATA_DIR)
    quiz_handler = QuizHandler(json_dir=DATA_DIR)

    api_handler.download_questions(q_type="multiple")


if __name__ == "__main__":
    main()
