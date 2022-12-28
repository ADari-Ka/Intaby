# static analysis: ignore[import_failed]
from sqlalchemy import Column, MetaData, Integer, String, ForeignKey, Text, Enum, Table, Boolean
from sqlalchemy.orm import registry
from sqlalchemy.orm import mapper, relationship

from domain import model


# Base = declarative_base()
mapper_registry = registry()
metadata = mapper_registry.metadata

# relations between tables:
#   - To find quizzes: search quizzes table by user_id
#   - To find questions: search question table by quiz_id
#   - To find answers: search answers table by question_id

# TODO: proper comments for tables

# Table for users
user_table = Table("users", metadata,
                   Column('id', Integer, primary_key=True, autoincrement=True),
                   Column('name', Text),
                   Column('surname', Text),
                   Column('email', Text, unique=True),
                   Column('password', Text))

# Table for quizzes
quiz_table = Table("quizzes", metadata,
                   Column('id', Integer, primary_key=True, autoincrement=True),
                   Column('user_id', Integer, ForeignKey('users.id', ondelete="CASCADE")),
                   Column('name', Text))

# Table for questions
question_table = Table("questions", metadata,
                       Column('id', Integer, primary_key=True, autoincrement=True),
                       Column('quiz_id', Integer, ForeignKey('quizzes.id', ondelete="CASCADE")),
                       Column('question_type', Text),
                       Column('text', Text),
                       Column('time', Integer))

# Table for answers
answer_table = Table("answers", metadata,
                     Column('id', Integer, primary_key=True, autoincrement=True),
                     Column('question_id', Integer, ForeignKey('questions.id', ondelete="CASCADE")),
                     Column('text', Text),
                     Column('correct_answer', Boolean))


def start_mappers():
    question_mapper = mapper_registry.map_imperatively(model.Question, question_table)
    user_mapper = mapper_registry.map_imperatively(model.User, user_table)
    answer_mapper = mapper_registry.map_imperatively(model.Answer, answer_table)
    quiz_mapper = mapper_registry.map_imperatively(model.Quiz, quiz_table)


def create_all(engine):
    metadata.bind = engine
    metadata.create_all()


def delete_all(engine):
    metadata.drop_all(engine)


if __name__ == '__main__':
    start_mappers()
