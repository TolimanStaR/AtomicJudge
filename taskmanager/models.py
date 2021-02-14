from django.db import models


class Status(models.IntegerChoices):
    CHECKED = 2
    IN_PROCESS = 1
    NOT_CHECKED = 0


class Verdict(models.Choices):
    ACCEPTED = (Status.CHECKED, {'ru': 'Правильное решение', 'en': 'Accepted'})
    CHECKING = (Status.IN_PROCESS, {'ru': 'Проверяется', 'en': 'Checking'})
    QUEUED = (Status.NOT_CHECKED, {'ru': 'В очереди', 'en': 'Queued'})
    TECH_ERROR = (Status.CHECKED, {'ru': 'Произошел технический сбой', 'en': 'The technical error'})
    WRONG_FORMAT = (Status.CHECKED, {'ru': 'Неправильный формат файла', 'en': 'Wrong file format'})
    COMPILATION_ERROR = (Status.CHECKED, {'ru': 'Ошибка Компиляции', 'en': 'Compilation error'})
    RUNTIME_ERROR = (Status.CHECKED, {'ru': 'Ошибка во время исполнения', 'en': 'Runtime error'})
    TIME_LIMIT_EXPIRED = (Status.CHECKED, {'ru': 'Превышено ограничение по времени', 'en': 'Time linet expired'})
    MEMORY_LIMIT_EXPIRED = (Status.CHECKED, {'ru': 'Превышено ограничение по памяти', 'en': 'Memory limit expired'})


class Language(models.TextChoices):
    GNU_ASM = 'GNU Assembly Language'
    GNU_C_99 = 'GNU C99'
    GNU_C_11 = 'GNU C 11'
    GNU_CXX_11 = 'GNU C++ 11'
    GNU_CXX_14 = 'GNU C++ 14'
    GNU_CXX_17 = 'GNU C++ 17'
    PYTHON_2_7 = 'Python 2.7'
    PYTHON_3_8 = 'Python 3.8'
    PYPY = 'PyPy'
    JAVA_11 = 'Java 11'
    RUBY_2_7 = 'Ruby'
    KOTLIN = 'Kotlin'
    GOLANG = 'GoLang'
    CSHARP = 'C#'
    BASH = 'Bash'
    # LAMA = 'Lama'


class LanguageType(models.IntegerChoices):
    COMPILE = 0
    INTERPRET = 1


class CheckScript(models.Model):
    code = models.TextField()
    language = models.TextField(choices=Language)
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
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.AutoField()  # TODO: add f.k. to user model
    code = models.TextField()
    created = models.DateField(auto_now_add=True, )
    language = models.TextField(choices=Language.choices, )
    language_type = models.IntegerField(default=LanguageType.COMPILE)
    file_name = models.CharField(max_length=100)
    verdict = models.Field(choices=Verdict.choices, default=Verdict.QUEUED)
    status = models.IntegerField(choices=Status.choices, default=Status.NOT_CHECKED)
    serving_note = models.IntegerField(default=0)


class TestCase(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='tests')
    test_value = models.TextField()
    answer = models.TextField(default=str(), blank=True)
