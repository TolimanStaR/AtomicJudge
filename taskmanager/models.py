from django.utils.translation import gettext_lazy as _
from django.db import models


class Status(models.TextChoices):
    CHECKED = 'a'
    IN_PROCESS = 'b'
    NOT_CHECKED = 'c'


class Verdict(models.TextChoices):
    ACCEPTED = 'AC', _(' Правильно решение')
    ERROR = 'ERR', _('Ошибка')
    IN_PROGRESS = 'IN_P', _('Выполняется')
    QUEUED = 'Q', _('В очереди')


class Language(models.TextChoices):
    GNU_ASM = 'ASM', _('GNU Assembly Language')
    GNU_C_99 = 'C99', _('GNU C99')
    GNU_C_11 = 'C11', _('GNU C 11')
    GNU_CXX_11 = 'C++11', _('GNU C++ 11')
    GNU_CXX_14 = 'C++14', _('GNU C++ 14')
    GNU_CXX_17 = 'C++17', _('GNU C++ 17')
    PYTHON_2_7 = 'Python2', _('Python 2.7')
    PYTHON_3_8 = 'Python3', _('Python 3.8')


language_extension: dict = {
    'ASM': 's',
    'C99': 'c',
    'C11': 'c',
    'C++11': 'cpp',
    'C++14': 'cpp',
    'C++17': 'cpp',
    'Python2': 'py',
    'Python3': 'py',
}


# PYPY = 'PyPy'
# JAVA_11 = 'Java 11'
# RUBY_2_7 = 'Ruby'
# KOTLIN = 'Kotlin'
# GOLANG = 'GoLang'
# CSHARP = 'C#'
# BASH = 'Bash'
# LAMA = 'Lama'


class LanguageType(models.IntegerChoices):
    COMPILE = 0
    INTERPRET = 1


class CheckScript(models.Model):
    code = models.TextField()
    language = models.TextField(choices=Language.choices)
    time_limit_seconds = models.IntegerField(default=2)
    memory_limit_seconds = models.IntegerField(default=128)


class TaskBase(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    input_description = models.TextField()
    output_description = models.TextField()
    time_limit_seconds = models.IntegerField(default=1)
    memory_limit_megabytes = models.IntegerField(default=128)
    has_answer_check_script = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Task(TaskBase):
    is_tested = models.BooleanField(default=False)


class SolutionCase(models.Model):
    # task = models.ForeignKey(Task, on_delete=models.CASCADE)
    # user = models.AutoField()  # TODO: add f.k. to user model
    code = models.TextField()
    # created = models.DateField(auto_now_add=True, )
    language = models.TextField(choices=Language.choices, )
    language_type = models.IntegerField(default=LanguageType.COMPILE)
    file_name = models.CharField(max_length=100)
    verdict = models.TextField(choices=Verdict.choices, )
    status = models.IntegerField(choices=Status.choices, default=Status.NOT_CHECKED)
    serving_note = models.IntegerField(default=0)


class TestCase(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='tests')
    test_value = models.TextField()
    answer = models.TextField(default=str(), blank=True)
