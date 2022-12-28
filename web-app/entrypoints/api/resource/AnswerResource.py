# static analysis: ignore[import_failed]
from flask import jsonify
from flask_restful import reqparse, abort, Resource
from adapters.repository import SqlAlchemyRepository, get_repo
from domain.model import Answer


class AnswerResource(Resource):
    def get(self, answer_id):
        repo = get_repo()
        answer = repo.get_answer(answer_id)
        return answer
