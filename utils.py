def prompt(message, questions):
    def format_question(question):
        key, item = question
        return f'{key}) {item} \n'

    def prompt_until_right_answer(answer, questions):
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

    formatted_questions = map(format_question, enumerate(questions, start=1))
    split = ''.join(formatted_questions)

    return prompt_until_right_answer(f'\n{colored(CmdColors.OKBLUE, message)}\n{split}> ', questions)


class CmdColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def colored(cmd_color, str):
    return f'{cmd_color}{str}{CmdColors.ENDC}'
