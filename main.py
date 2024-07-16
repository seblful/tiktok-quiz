import os

from modules.quiz import OpentdbAPIHandler, QuizHandler

HOME = os.getcwd()
DATA_DIR = os.path.join(HOME, 'data')


def main() -> None:
    # # Download questions
    # api_handler = OpentdbAPIHandler(json_dir=DATA_DIR)
    # api_handler.download_questions(q_type="multiple")
    # api_handler.download_questions(q_type="boolean")

    # Get question
    quiz_handler = QuizHandler(json_dir=DATA_DIR)
    question = quiz_handler.get_random_question(q_type="multiple")
    print(question)


if __name__ == "__main__":
    main()
