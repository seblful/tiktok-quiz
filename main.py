import os
import time

from modules.opentdb import OpentdbAPIHandler
from modules.game import GameCreator

HOME = os.getcwd()
JSON_DIR = os.path.join(HOME, 'data')
SOURCE_DIR = os.path.join(HOME, 'source')


def main() -> None:
    # # Download questions
    # api_handler = OpentdbAPIHandler(json_dir=JSON_DIR)
    # api_handler.download_questions(q_type="multiple")
    # time.sleep(60)
    # api_handler.download_questions(q_type="boolean")

    # Run game
    game_creator = GameCreator(json_dir=JSON_DIR,
                               source_dir=SOURCE_DIR,
                               screen_size=(468, 832))
    game_creator.run()


if __name__ == "__main__":
    main()
