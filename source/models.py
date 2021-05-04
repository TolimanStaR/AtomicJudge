import threading
import datetime
import os
import psycopg2
from django.db import models

from django.utils.translation import gettext_lazy as _


# This classes must be the same with similar in web-application


class TaskAnswerType(models.TextChoices):
    CONSTANT_ANSWER = 'CA', _('Constant answer')
    VARIABLE_ANSWER = 'VA', _('Variable answer')


class TaskExecuteType(models.TextChoices):
    JUST_RUN = 'run', _('Only run source')
    BUILD_AND_RUN = 'build && run', _('Build binary, then run it')


class Language(models.TextChoices):
    GNU_ASM = 'ASM', _('GNU Assembly Language')
    GNU_C99 = 'C99', _('GNU GCC C99')
    GNU_C11 = 'C11', _('GNU GCC C11')
    GNU_CXX_11 = 'C++11', _('GNU G++ C++ 11')
    GNU_CXX_14 = 'C++14', _('GNU G++ C++ 14')
    GNU_CXX_17 = 'C++17', _('GNU G++ C++ 17')
    GNU_CXX_20 = 'C++20', _('GNU G++ C++ 20')
    PYTHON_2_7 = 'Python2', _('Python v2.7')
    PYTHON_3_9 = 'Python3', _('Python v3.9.4')


class Status(models.TextChoices):
    WAIT_FOR_CHECK = 'WAIT', _('Waiting for check')
    QUEUED = 'QUEUED', _('Queued')
    IN_PROGRESS = 'IN PROGRESS', _('In progress')
    CHECK_FAILED = 'FAILED', _('Check failed')
    CHECK_SUCCESS = 'SUCCESS', _('Check success')


class Verdict(models.TextChoices):
    EMPTY_VERDICT = 'NO VERDICT', _('No verdict')
    WRONG_FILE_FORMAT = 'WRONG FILE FORMAT', _('Wrong format of file')
    FILE_TOO_BIG = 'FILE TOO BIG', _('File has too large size')
    BUILD_FAILED = 'BUILD FAILED', _('Build failed')
    RUNTIME_ERROR = 'RUNTIME ERROR', _('Runtime error')
    TIME_LIMIT_ERROR = 'TIME LIMIT ERROR', _('Time limit error')
    MEMORY_LIMIT_ERROR = 'MEMORY LIMIT ERROR', _('Memory limit error')
    WRONG_ANSWER = 'WRONG ANSWER', _('Wrong answer')
    CORRECT_SOLUTION = 'CORRECT SOLUTION', _('Correct solution')


# End of django classes


class SingletonMixin(object):
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def instance(cls):
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls()
        return cls.__singleton_instance


class DataBase(SingletonMixin):
    def __init__(self):
        passwd = os.getenv('COURSEWORK2_DB_PASSWORD')
        self.connection = psycopg2.connect(dbname='age-of-python',
                                           user='postgres',
                                           password=f'{passwd}',
                                           host='185.139.70.166')
        self.cursor = self.connection.cursor()

    def execute(self, sql_request, *params):
        self.cursor.execute(sql_request, params)

    def result(self):
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()

    def close_connection(self):
        self.connection.close()

    def __str__(self):
        pass


class Test(object):
    def __init__(self, **kwargs):
        self.id = None
        self.task_id = None
        self.set_attributes(**kwargs)

    def set_attributes(self, **kwargs):
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

    def __str__(self):
        return f'class Test\n' \
               f'id: {self.id}\n' \
               f'task id: {self.task_id}'


class CodeFile(object):
    def __init__(self, **kwargs):
        self.id = None
        self.solution: Solution or None = None

        self.set_attributes(**kwargs)

    def set_attributes(self, **kwargs):
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

    def __str__(self):
        return f'Class CodeFile \n' \
               f'id: {self.id}'

    def get_solution(self):
        return self.solution

    def set_solution(self, solution: 'Solution'):
        self.solution = solution


class Solution(object):
    def __init__(self, **kwargs):
        self.event_type = None
        self.task_id = None
        self.code_file_id = None
        self.verdict = None
        self.status = None
        self.id = None
        self.code_file: CodeFile or None = None

        self.set_attributes(**kwargs)

    def set_attributes(self, **kwargs):
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

    def __str__(self):
        return f'Class Solution \n' \
               f'id: {self.id}\n' \
               f'status: {self.status}\n' \
               f'verdict: {self.verdict}'

    def __update__(self, field, value):
        sql_request = f'''UPDATE management_solution
                        SET {field} = '{value}'
                        WHERE id = {self.id};'''
        db = DataBase()
        db.execute(sql_request=sql_request)
        db.commit()

    def get_code_file_id(self):
        return self.code_file_id

    def get_code_file(self):
        return self.code_file

    def set_code_file(self, code_file: CodeFile):
        self.code_file = code_file


class Event(object):

    def __init__(self, solution: Solution, tests: "Any iterable"):
        self.solution = solution
        self.tests = tests

    def set_attributes(self, **kwargs):
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

    def get_all_tests(self):
        return self.tests

    def __str__(self):
        return f'class Event\n' \
               f'event type: {self.solution.event_type}\n' \
               f'solution id: {self.solution.id}\n' \
               f'task id: {self.solution.task_id}\n' \
               f'~ with {len(self.tests)} tests'
