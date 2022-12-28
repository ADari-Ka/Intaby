# static analysis: ignore[import_failed]
from entrypoints.api.resource import AnswerResource, QuizResource, QuestionResource, UserResource

from flask_restful import Api


def api_initialization(app) -> Api:
    api = Api(app)
    api.add_resource(UserResource.UserLoginResource, '/api/user/login')
    api.add_resource(UserResource.UserRegistrationResource, '/api/user/register')

    api.add_resource(QuizResource.QuizResource, '/api/user/<int:user_id>/quiz/<int:quiz_id>')
    api.add_resource(QuizResource.QuizListResource, '/api/user/<int:user_id>/quiz')

    api.add_resource(QuestionResource.QuestionResource, '/api/quiz/<int:quiz_id>/question/<int:question_id>')

    return api
