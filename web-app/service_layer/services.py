# static analysis: ignore[import_failed]
from domain import model


# user_from gets args and creates User class
# user_args should contain following:
#   name
#   surname
#   email
#   password
def user_from(user_args: dict) -> model.User:
    user_name = user_args['name']
    user_surname = user_args['surname']
    user_email = user_args['email']
    user_password = user_args['password']

    return model.User(
        name=user_name,
        surname=user_surname,
        email=user_email,
        password=user_password
    )


def quiz_from(quiz_args: dict, user_id: int) -> model.Quiz:
    quiz = model.Quiz(
        quiz_name=quiz_args["name"],
        user_id=user_id
    )
    return quiz


def questions_of_quiz_creation_from(quiz_args: dict, quiz_id: int) -> [(model.Question, dict)]:
    questions = [
        (model.Question(
            question_type=question_args["question_type"],
            text=question_args["text"],
            time_limit=question_args["time"],
            quiz_id=quiz_id
        ), question_args["answers"])
        for question_args in quiz_args["questions"]
    ]
    # return quiz_args["questions"]
    # for question_args in quiz_args["questions"]:
    #     questions.append((model.Question(
    #         question_type=question_args["question_type"],
    #         text=question_args["text"],
    #         time_limit=question_args["time"],
    #         quiz_id=quiz_id),
    #                       question_args["answers"]))

    return questions


def answers_for_one_question_of_quiz_creation_from(answers_args: dict, question_id) -> [model.Answer]:
    answers = [
        model.Answer(
            text=answer_args["text"],
            correct_answer=answer_args["correct_answer"],
            question_id=question_id
        )
        for answer_args in answers_args
    ]
    return answers


def email_and_pass_from(args: dict) -> (str, str):
    return args['email'], args['password']


def user_from(user_args) -> model.User:
    return model.User(
        name=user_args["name"],
        surname=user_args["surname"],
        email=user_args["email"],
        password=user_args["password"]
    )
