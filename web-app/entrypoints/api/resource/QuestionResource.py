# static analysis: ignore[import_failed]
from flask import jsonify
from flask_restful import reqparse, abort, Resource
from adapters.repository import SqlAlchemyRepository, get_repo
from domain.model import Question, QuestionTypes

parser = reqparse.RequestParser()
parser.add_argument('answer', required=True)


class QuestionResource(Resource):
    def get(self, quiz_id, question_id):
        repo = get_repo()
        question = repo.get_question(question_id)
        return question

    def post(self, quiz_id, question_id):
        args = parser.parse_args()
        repo = get_repo()

        chosen_answer = args['answer']
        # TODO: Find all answers to questions, and find the chosen one
