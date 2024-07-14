from modules.quiz import OpentdbAPIHandler


def main() -> None:
    api_handler = OpentdbAPIHandler()

    api_handler.download_questions(q_type="multiple")


if __name__ == "__main__":
    main()
