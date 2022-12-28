# static analysis: ignore[import_failed]
import flask
from flask import jsonify, make_response
from flask_restful import reqparse, abort, Resource
from adapters.repository import SqlAlchemyRepository, get_repo

from domain.model import User

from service_layer import services

from sqlalchemy.exc import IntegrityError

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', required=True)
login_parser.add_argument('password', required=True)

registration_parser = reqparse.RequestParser()
registration_parser.add_argument('name', required=True)
registration_parser.add_argument('surname', required=True)
registration_parser.add_argument('email', required=True)
registration_parser.add_argument('password', required=True)


def check_for_credentials(args: dict) -> int:
    email, password = services.email_and_pass_from(args)

    repo = get_repo()
    user = repo.get_user_by_email(email)

    if not user:
        abort(404, message="Unauthorized")

    if not user.password == password:
        abort(404, message="Unauthorized")

    return user.id


def abort_if_user_already_exists(email):
    repo = get_repo()

    user = repo.get_user_by_email(email)

    if user:
        abort(403, message="User already exists")


def abort_if_user_not_found(user_id: int, args: dict):
    email, password = services.email_and_pass_from(args)

    repo = get_repo()
    user = repo.get_user_by_id(user_id)
    if not user or user.email != email or user.password != password:
        abort(404, message="Unauthorized")


class UserLoginResource(Resource):
    def post(self):
        args = login_parser.parse_args()

        user_id = check_for_credentials(args)

        return {"user_id": user_id}


class UserRegistrationResource(Resource):
    def post(self):
        args = registration_parser.parse_args()
        repo = get_repo()

        user = services.user_from(args)

        # abort_if_user_already_exists(user.email)
        try:
            repo.add_user(user)
            return make_response("User created", 201)

        except IntegrityError:
            repo.session.rollback()
            return make_response("User already exists", 403)
