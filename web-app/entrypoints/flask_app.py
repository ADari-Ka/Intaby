# static analysis: ignore[import_failed]
import json

from flask import Flask, request, render_template
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from domain import model
from adapters import orm, repository
from service_layer import services
from entrypoints.api import api_initialization
from tests import test_orm

engine = create_engine(config.get_postgres_uri())
get_session = sessionmaker(bind=engine)
repository.initialize_repo(get_session())
orm.start_mappers()

# To delete all tables
# orm.delete_all(engine)

orm.create_all(engine)
app = Flask(__name__, template_folder='./../static/templates')
api = api_initialization.api_initialization(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/')
def main_page():
    return render_template("main_page.html")


@app.route('/login')
def login_page():
    return render_template('authorization_page.html')


@app.route('/register')
def registration_page():
    return render_template("registration_page.html")


# [will be deleted]
@app.route('/lobby')
def lobby_page():
    return render_template("waiting_hall.html")


# For tests through docker
@app.route('/tests/users')
def test():
    repo = repository.get_repo()

    new_items = list()
    for item in repo.get_users():
        new_items.append(item.to_dict())

    return json.dumps({"items": new_items})


@app.route('/tests/user_creation')
def test_user_creation():
    repo = repository.get_repo()

    test_orm.test_add_user(repo)

    return "<p>OK</p>"


@app.route('/tests/quizzes')
def test_quizzes_list():
    repo = repository.get_repo()

    new_items = list()
    for item in repo.get_quizzes():
        new_items.append(item.to_dict())

    return json.dumps({"items": new_items})


@app.route('/tests/get_user_by_email/<email>')
def test_user_by_email(email):
    repo = repository.get_repo()

    user = repo.get_user_by_email(email)
    return json.dumps({"user": user.to_dict()})


@app.route('/tests/answers')
def test_answers_list():
    repo = repository.get_repo()

    dict_items = []
    for item in repo.get_answers():
        dict_items.append(item.to_dict())
    return json.dumps({"answers": dict_items})
