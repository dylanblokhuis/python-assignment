from typing import List
from colors import Colors


class QuestionPrompter:
    questions: List[str] = []

    def __init__(self, questions):
        self.questions = questions

    def prompt(self, message):
        def format_question(question):
            key, item = question
            return f'{key}) {item} \n'

        def colored_prompt(color: str, str):
            return f'{color}{str}{Colors.ENDC}'

        questions = self.get_questions()

        # format the questions by adding a number infront like:
        # 1) First question
        # 2) Second question
        formatted_questions = map(format_question, enumerate(questions, start=1))
        split = ''.join(formatted_questions)

        blue_colored_message = colored_prompt(Colors.BLUE, message)
        return self.__prompt_until_right_answer(f'\n{blue_colored_message}\n{split}> ')

    def __prompt_until_right_answer(self, answer):
        questions = self.get_questions()

        while True:
            question = None

            try:
                user_answer = int(input(answer))
            except ValueError:
                print("That answer is invalid please try again.")
                continue

            for key, item in enumerate(questions, start=1):
                if key == user_answer:
                    question = item

            if not question:
                print("That answer doesn't match any questions.")
                continue
            else:
                return question

    def get_questions(self):
        return self.questions

    def set_questions(self, questions):
        self.questions = questions
