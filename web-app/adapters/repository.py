# static analysis: ignore[import_failed]

from domain import model

__repo = None


# drafts
# class AbstractRepository(ABC):
#     @abstractmethod
#     def add(self, thing):
#         raise NotImplementedError
#
#     @abstractmethod
#     def get(self, ref):
#         raise NotImplementedError


# repository pattern to structure code
# SqlAlchemy repository to access db
# TODO: comments
# TODO: command for put, delete request
class SqlAlchemyRepository:
    def __init__(self, session):
        self.session = session

    def add_user(self, user: model.User):
        self.session.add(user)
        self.session.commit()

    def get_user_by_id(self, user_id):
        return self.session.query(model.User).filter_by(id=user_id).one()

    def get_user_by_email(self, email):
        return self.session.query(model.User).filter_by(email=email).one()

    def delete_user(self, user: model.User):
        self.session.delete(user)
        self.session.commit()

    # Working with quizzes
    def add_quiz(self, quiz: model.Quiz) -> int:
        self.session.add(quiz)
        self.session.commit()
        return quiz.id

    def get_quiz(self, quiz_id):
        return self.session.query(model.Quiz).filter_by(id=quiz_id).one()

    def put_quiz(self, quiz: model.Quiz):
        # self.session.query(model.Quiz).f
        raise NotImplemented

    def delete_quiz(self, quiz: model.Quiz):
        self.session.delete(quiz)
        self.session.commit()

    def list_quizzes(self, user_id):
        return self.session.query(model.Quiz).filter_by(user_id=user_id).all()

    # Working with questions
    def add_question(self, question: model.Question):
        self.session.add(question)
        self.session.commit()
        return question.id

    def get_question(self, question_id):
        return self.session.query(model.Question).filter_by(id=question_id).one()

    def delete_question(self, question: model.Question):
        self.session.delete(question)
        self.session.commit()

    def list_questions(self, quiz_id):
        return self.session.query(model.Question).filter_by(quiz_id=quiz_id).all()

    # Working with answers
    def add_answer(self, answer: model.Answer):
        self.session.add(answer)
        self.session.commit()
        return answer.id

    def get_answer(self, answer_id):
        return self.session.query(model.Answer).filter_by(id=answer_id).one()

    def delete_answer(self, answer: model.Answer):
        self.session.delete(answer)
        self.session.commit()

    def list_answers(self, question_id):
        return self.session.query(model.Answer).filter_by(question_id=question_id).all()

    # -- for test
    def get_users(self):
        return self.session.query(model.User).all()

    def get_quizzes(self):
        return self.session.query(model.Quiz).all()

    def get_answers(self):
        return self.session.query(model.Answer).all()

    def get_questions(self):
        return self.session.query(model.Question).all()


# Testing Repository
class FakeRepository:
    def add_user(self, user: model.Quiz):
        print(f"Adding user {user}")

    def get_user(self, user_id):
        print(f"Getting user {user_id}")

    # Working with quizzes
    def add_quiz(self, quiz: model.Quiz):
        print(f"Adding quiz {quiz}")

    def get_quiz(self, quiz_id):
        print(f"Getting quiz {quiz_id}")

    def list_quizzes(self, user_id):
        print(f"Getting list of quizzes of user {user_id}")

    def put_quiz(self, quiz: model.Quiz):
        print(f"Changing quiz using {quiz}")

    def delete_quiz(self, quiz_id):
        print(f"deletion of quiz {quiz_id}")

    # Working with questions
    def add_question(self, question: model.Question):
        print(f"Adding question {question}")

    def get_question(self, question_id):
        print(f"Getting question {question_id}")

    def list_questions(self, quiz_id):
        print(f"Getting list of question of quiz {quiz_id}")

    def put_question(self, question: model.Question):
        print(f"Changing quiz using {question}")

    def delete_question(self, question_id):
        print(f"deletion of question {question_id}")

    # Working with answers
    def add_answer(self, answer: model.Answer):
        print(f"Adding answer {answer}")

    def get_answer(self, answer_id):
        print(f"Getting answer {answer_id}")

    def list_answers(self, question_id):
        print(f"Getting list of answers of question {question_id}")

    def put_answer(self, answer: model.Quiz):
        print(f"Changing answer using {answer}")

    def delete_answer(self, answer_id):
        print(f"deletion of answer {answer_id}")


# Testing
__repo = FakeRepository()


# To access repo from different modules
def initialize_repo(session):
    global __repo

    if not __repo or __repo.__class__ == FakeRepository:
        __repo = SqlAlchemyRepository(session)


def get_repo():
    global __repo
    return __repo
