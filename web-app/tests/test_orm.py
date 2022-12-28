# static analysis: ignore[import_failed]
from adapters import repository
from domain import model


# Unit tests can be written only for user or quiz (With user)
# Because we use foreign key to link all info in db

def test_add_user(repo):
    new_user = model.User("Fedor", "Surname", "fedya@gg.ru", "CoolPass")

    repo.add_user(new_user)
    db_user = repo.session.query(model.User).filter_by(email=new_user.email).one()

    assert db_user == new_user

    repo.delete_user(new_user)


def test_add_and_quiz(repo):
    new_user = model.User("Fedor", "Surname", "fedya@gg.ru", "CoolPass")
    user_id = repo.add_user(new_user)

    new_quiz = model.Quiz(quiz_name="Quiz name", user_id=user_id)
    quiz_id = repo.add_quiz(new_quiz)

    db_quiz = repo.get_quiz(quiz_id)

    assert db_quiz == new_quiz

    repo.delete_user(new_user)


def test_add_and_question(repo):
    new_user = model.User("Fedor", "Surname", "fedya@gg.ru", "CoolPass")
    user_id = repo.add_user(new_user)

    new_quiz = model.Quiz(quiz_name="Quiz name", user_id=user_id)
    quiz_id = repo.add_quiz(new_quiz)

    question = model.Question(question_type="poll", text="questions1", time_limit=60, quiz_id=quiz_id)
    question_id = repo.add_questions(question1)

    db_question = repo.get_question(question_id)

    assert db_question == question

    repo.delete_user(new_user)


def test_add_and_answer(repo):
    new_user = model.User("Fedor", "Surname", "fedya@gg.ru", "CoolPass")
    user_id = repo.add_user(new_user)

    new_quiz = model.Quiz(quiz_name="Quiz name", user_id=user_id)
    quiz_id = repo.add_quiz(new_quiz)

    question = model.Question(question_type="poll", text="questions1", time_limit=60, quiz_id=quiz_id)
    question_id = repo.add_questions(question)

    answer = model.Answer(text="Hello", correct_answer=True, question_id=question_id)
    answer_id = repo.add_answer(answer)

    db_answer = repo.get_answer(answer_id)

    assert db_answer == answer

    repo.delete_user(new_user)
