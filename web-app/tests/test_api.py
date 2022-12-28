# static analysis: ignore[import_failed]
import json

from requests import get, post, delete, put


def test_quizzes_post_request():
    answers1 = [
        {"text": "Hello", "correct_answer": True},
        {"text": "World", "correct_answer": False}
    ]
    question1 = {"question_type": "poll",
                 "text": "questions1",
                 "time": 60,
                 "answers": answers1}

    answers2 = [
        {"text": "Hello", "correct_answer": True},
        {"text": "World", "correct_answer": False}
    ]

    question2 = {
        "question_type": "quiz",
        "text": "questions2",
        "time": 15,
        "answers": answers2
    }

    quiz_post_request_body = {
        "questions": [question1, question2],
        "name": "Quiz name"
    }

    # print(type(quiz_post_request_body["questions"]))

    url = "http://127.0.0.1:8888/api/user/1/quiz"
    assert post(url, json=quiz_post_request_body,
                headers={"Content-Type": "application/json"}).status_code == 201


def test_quiz_get_request():
    url = "http://127.0.0.1:8888/api/user/1/quiz/1"
    assert get(url).status_code == 200


# def test_quiz_delete_request():
#     quiz_post_request_body = {
#         "questions": {"question1": {"Hello": True, "World": True}, "question2": {"Hello": True, "World": True}},
#         "name": "Quiz name"
#     }
#     url = "http://127.0.0.1:8888/api/user/1/quiz"
#
#     post(url, data=json.dumps(quiz_post_request_body), headers={"Content-Type": "application/json"})
#
#     assert delete(url + "/1").status_code == 200


def test_quizzes_get_request():
    url = "http://127.0.0.1:8888/api/user/1/quiz"

    assert get(url).status_code == 200


def test_quiz_put_request():
    url = "http://127.0.0.1:8888/api/user/1/quiz/1"

    answers1 = [
        {"text": "Hello", "correct_answer": False},
        {"text": "Worldzzz", "correct_answer": False}
    ]
    question1 = {"question_type": "poll",
                 "text": "questions1",
                 "time": 60,
                 "answers": answers1}

    answers2 = [
        {"text": "Hello", "correct_answer": True},
        {"text": "World", "correct_answer": False}
    ]

    question2 = {
        "question_type": "quiz",
        "text": "questions2zzz",
        "time": 15,
        "answers": answers2
    }

    quiz_put_request_body = {
        "questions": [question1, question2],
        "name": "Quiz recreated name"
    }

    assert put(url, json=quiz_put_request_body, headers={"Content-Type": "application/json"}).status_code == 200


def test_user_login_request():
    url = "http://127.0.0.1:8888/api/user/login"

    body = {"email": "vikochka_kruk@mail.ru",
            "password": "123"}

    assert post(url, json=body).status_code == 200


def test_user_post_request():
    url = "http://127.0.0.1:8888/api/user/register"

    user_post_request_body = {
        'name': 'Il',
        'surname': 'hello',
        'email': 'il@k.r',
        'password': 'strong_pass'
    }
    assert post(url, json=user_post_request_body, headers={"Content-Type": "application/json"}).status_code == 201


def test_question_get_request():
    url = "http://127.0.0.1:8888/api/quiz/1/question/2"
    assert get(url).status_code == 200


def test_question_post_request():
    url = "http://127.0.0.1:8888/api/quiz/1/question/2"

    question_post_request_body = {"answers": ["Incorrect answer", "Correct answer"]}
    assert post(url, json=question_post_request_body, headers={"Content-Type": "application/json"}).status_code == 201


def test_quiz_delete_request():
    url = "http://127.0.0.1:8888/api/user/1/quiz/1"

    assert delete(url).status_code == 200


# print(test_user_post_request())
# print(test_quiz_delete_request())
# print(test_quiz_put_request())
# print(test_quizzes_post_request())
# print(test_quiz_get_request())
# print(test_user_login_request())
# print(test_question_get_request())
# print(test_user_get_request())

# print(str([{"Hello": True, "World": False}]))
