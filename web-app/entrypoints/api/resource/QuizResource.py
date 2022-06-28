from flask import jsonify, make_response
from flask_restful import reqparse, abort, Resource
from adapters.repository import SqlAlchemyRepository, get_repo
from domain.model import Quiz
from service_layer import services

quiz_creation_parser = reqparse.RequestParser()
quiz_creation_parser.add_argument('name', required=True)
quiz_creation_parser.add_argument('questions', type=dict, action="append", required=True)

quiz_get_parser = reqparse.RequestParser()
quiz_get_parser.add_argument('email', required=True)
quiz_get_parser.add_argument('password', required=True)


def check_for_credentials(args: dict):
    email, password = services.email_and_pass_from(args)

    repo = get_repo()
    user = repo.get_user_by_email(email)

    if not user:
        abort(404, message="Unauthorized")

    if not user.password == password:
        abort(404, message="Unauthorized")


def abort_if_user_not_found(user_id: int):
    repo = get_repo()
    user = repo.get_user_by_id(user_id)
    if not user:
        abort(404, message="Unauthorized")


def abort_if_quiz_not_found(quiz_id):
    repo = get_repo()
    quiz = repo.get_quiz(quiz_id)

    if not quiz:
        abort(404, message="Quiz is not found")


class QuizResource(Resource):
    def get(self, user_id, quiz_id):
        abort_if_quiz_not_found(quiz_id)

        repo = get_repo()
        quiz = repo.get_quiz(quiz_id)

        if quiz.user_id != user_id:
            abort(403, message="You are not allowed to get this information")

        questions = repo.list_questions(quiz_id)
        questions_list = []
        # assert len(questions) != 0
        for question in questions:
            questions_list.append(question.to_dict())

            answers_list = []
            answers = repo.list_answers(question.id)
            for answer in answers:
                answers_list.append(answer.to_dict())
            questions_list[-1]["answers"] = answers_list

        quiz_dict = quiz.to_dict()
        quiz_dict["questions"] = questions_list
        return make_response(quiz_dict, 200)

    def put(self, user_id, quiz_id):
        abort_if_quiz_not_found(quiz_id)

        args = quiz_creation_parser.parse_args()
        check_for_credentials(args)

        repo = get_repo()
        repo.put_quiz(Quiz(quiz_id=quiz_id, name=args['name'], user_id=args['user_id']))

        # TODO: Putting questions + answers

        return jsonify({"success": "OK"})

    def delete(self, user_id, quiz_id):
        abort_if_quiz_not_found(quiz_id)

        repo = get_repo()

        quiz = repo.get_quiz(quiz_id)

        if quiz.user_id != user_id:
            abort(403, message="You are not allowed to perform this action")

        repo.delete_quiz(quiz)
        # questions = repo.list_questions(quiz_id)
        #
        # for question in questions:
        #
        #     answers = repo.list_answers(question.id)
        #     for answer in answers:
        #         repo.delete_answer(answer)
        #     repo.delete_question(question)

        return make_response("Quiz deleted", 200)


class QuizListResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)

        repo = get_repo()
        quizzes = repo.list_quizzes(user_id)
        return make_response({"quizzes": [quiz.to_dict() for quiz in quizzes]}, 200)

    def post(self, user_id):
        args = quiz_creation_parser.parse_args()
        # return make_response(str(args), 404)
        abort_if_user_not_found(user_id)

        repo = get_repo()

        quiz = services.quiz_from(args, user_id)
        quiz_id = repo.add_quiz(quiz)

        questions_and_answers = services.questions_of_quiz_creation_from(args, quiz_id)
        # return make_response(str(questions_and_answers), 404)

        for (question, answers_args) in questions_and_answers:
            question_id = repo.add_question(question)
            for answers in services.answers_for_one_question_of_quiz_creation_from(answers_args, question_id):
                repo.add_answer(answers)

        return make_response("Quiz created", 201)
