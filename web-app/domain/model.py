import enum
from typing import List, NewType

# Types declaration

# For user
Name = NewType('Name', str)
Surname = NewType('Surname', str)
Email = NewType('Email', str)
Password = NewType('Password', str)

# For quiz
QuizId = NewType('QuizId', int)
QuizName = NewType('QuizName', str)

# For question
QuestionAnswer = NewType('QuestionAnswers', str)
QuestionDescription = NewType('QuestionDescription', str)


class Answer:
    def __init__(self, question_id: int, text: QuestionAnswer, correct_answer: bool):
        self.text = text
        self.correct_answer = correct_answer
        self.question_id = question_id

    def to_dict(self):
        return {
            "text": self.text,
            "correct_answer": self.correct_answer,
            "question_id": self.question_id
        }


# Possible types of question in a quiz
class QuestionTypes(enum.Enum):
    poll = "poll"
    quiz = "quiz"


# Question class, to store information about question:
#   question type, description, possible answers, and correct answers
class Question:
    def __init__(self, question_type: str, text: QuestionDescription, quiz_id: int, time_limit: int):
        self.question_type = question_type
        self.text = text
        self.quiz_id = quiz_id
        self.time = time_limit

    def to_dict(self):
        return {
            "quiz_id": self.quiz_id,
            "text": self.text,
            "question_type": self.question_type,
            "time": self.time
        }


# Quiz class,
class Quiz:
    def __init__(self, quiz_name: QuizName, user_id: int = 0):
        self.name = quiz_name
        self.user_id = user_id

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name
        }


# User class, to manage stored in db information through nickname/email
class User:
    def __init__(self, name: Name, surname: Surname, email: Email, password: Password):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "password": self.password
        }
