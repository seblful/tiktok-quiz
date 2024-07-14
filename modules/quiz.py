import os
import json
import requests
import time
import random

from typing import List


class OpentdbAPIHandler:
    def __init__(self,
                 json_dir: str) -> None:
        self.json_dir: str = json_dir

    def download_questions(self, q_type: str, amount: int = 50) -> None:
        # Get token
        response_token = requests.get(
            "https://opentdb.com/api_token.php?command=request")
        session_token = response_token.json()["token"]

        # API endpoint
        url = f"https://opentdb.com/api.php?amount={
            amount}&type={q_type}&token={session_token}"

        # Initialize an empty list to store the questions
        questions: List[int] = []

        # Retrieve questions in batches of amount
        while True:
            # Make the API request
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                # Load the JSON data
                data = json.loads(response.text)

                # Check if the API request was successful
                if data['response_code'] == 0:
                    # Add the questions to the list
                    questions.extend(data['results'])
                    print(f"It was downloaded {len(questions)} questions.")

                    # Check if there are more questions to retrieve
                    if len(data['results']) < amount:
                        break

                    # Delay for 5 seconds to avoid exceeding the rate limit
                    time.sleep(5)

                # Token Empty Session Token has returned all possible questions
                elif data["response_code"] == 4:
                    break

                elif data["response_code"] == 5:
                    print("Rate limit exceeded. Waiting for 10 seconds...")
                    time.sleep(10)
            else:
                print(f"Error: {response.status_code}")
                break

        # Save questions
        self.save_json(q_type=q_type,
                       questions=questions)

    def save_json(self, q_type: str,  questions: str) -> None:
        # Save the questions to a JSON file
        json_path: str = os.path.join(
            self.json_dir, f"trivia_questions_{q_type}.json")
        with open(json_path, "w") as file:
            json.dump(questions, file, indent=2)

        print(f"Questions with {q_type} type was saved.")


class QuizHandler:
    def __init__(self,
                 json_dir: str) -> None:
        self.json_dir = json_dir

        # Indexes that was used before
        self.multiple_idxs: List[int] = []
        self.boolean_idxs: List[int] = []

    def load_json(self, q_type: str):
        pass

    def get_random_question(self):
        pass
