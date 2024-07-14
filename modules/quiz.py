import requests
import json
import time

from typing import List


class OpentdbAPIHandler:
    def __init__(self) -> None:
        pass

    def download_questions(self, q_type: str, amount: int = 50) -> None:
        # API endpoint
        url = f"https://opentdb.com/api.php?amount={amount}&type={q_type}"

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

                    # Update the URL to retrieve the next batch of questions
                    url = f"https://opentdb.com/api.php?amount={amount}&type={q_type}&page={
                        len(questions)//amount}"

                    # Delay for 5 seconds to avoid exceeding the rate limit
                    time.sleep(5)
                else:
                    print(f"Error: {data['response_message']}")
                    break
            elif response.status_code == 429:
                print("Rate limit exceeded. Waiting for 60 seconds...")
                time.sleep(60)
            else:
                print(f"Error: {response.status_code}")
                break

        # Save questions
        self.save_json(q_type=q_type,
                       questions=questions)


def save_json(self, q_type: str,  questions: str) -> None:
    # Save the questions to a JSON file
    with open(f"trivia_questions_{q_type}.json", "w") as file:
        json.dump(questions, file, indent=2)

    print(f"Questions with {q_type} type was saved.")


class QuizHandler:
    def __init__():
        pass
