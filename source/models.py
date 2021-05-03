import threading
import datetime
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


class CodeFile(object):
    def __init__(self, **kwargs):
        pass


class Solution(object):
    def __init__(self, **kwargs):
        print(kwargs)

    def __str__(self):
        return f'Solution object {id(self)}'

    def __update__(self, field, value):
        pass
