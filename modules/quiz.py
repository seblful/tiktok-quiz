import os
import json
import time
import random

import requests
import html

from typing import List, Dict


class OpentdbAPIHandler:
    def __init__(self,
                 json_dir: str) -> None:
        self.json_dir: str = json_dir

        # Index
        self.index: int = 0

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

                    # Edit data
                    data = self.edit_data(data=data)

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

    def edit_data(self, data: List[Dict[str, str]]) -> List[Dict[str, str]]:
        # Edit data
        for i in range(len(data["results"])):
            # Reformat text of the questions and answers
            # Question
            data["results"][i]['question'] = html.unescape(
                data["results"][i]['question'])
            # Correct answer
            data["results"][i]["correct_answer"] = html.unescape(
                data["results"][i]["correct_answer"])
            # Incorrect answers
            for j in range(len(data["results"][i]["incorrect_answers"])):
                data["results"][i]["incorrect_answers"][j] = html.unescape(
                    data["results"][i]["incorrect_answers"][j])

            # Add index
            data["results"][i]['index'] = self.index
            self.index += 1

        return data

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
