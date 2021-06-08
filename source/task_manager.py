# todo: add hash sum to judge solution file name on web-app side cuz it can break everything

import os
import shutil
import subprocess
from typing import List

import source.models
from .service import sequence_to_dict

from .static import *

from .config import BUILD_SOURCE_MAX_TIME, SQL_GET_TASK_ATTRIBUTE, SQL_GET_CODE_FILE


class TaskManager(object):
    env_dir: str = 'environment'
    input_file_name: str = 'input.in'
    output_file_name: str = 'output.out'

    def __init__(self, event: source.models.Event):
        self.working_dir = os.getcwd()
        self.solution = event.solution
        self.code_file: source.models.CodeFile = event.code_file
        self.tests = event.tests

        self.judge_solution_source: source.models.CodeFile = source.models.CodeFile()

    def prepare_environment(self):
        env_path: str = os.path.join(self.working_dir, self.env_dir)
        if os.path.exists(env_path):
            shutil.rmtree(env_path)

        os.mkdir(env_path)

        code_file: str = os.path.join(env_path, self.code_file.file_name)
        input_file: str = os.path.join(env_path, self.input_file_name)
        output_file: str = os.path.join(env_path, self.output_file_name)

        __code = open(code_file, write_mode)
        __code.write(self.code_file.code)
        __code.close()

        __input = open(input_file, write_mode)
        __input.close()

        __output = open(output_file, write_mode)
        __output.close()

        db = source.models.DataBase()
        db.execute(SQL_GET_CODE_FILE, self.__get_task_solution_file_id__())
        code_file_attributes = {}
        for result in db.result():
            code_file_attributes = sequence_to_dict(result, class_CodeFile_attributes)
        code_file_obj: source.models.CodeFile = source.models.CodeFile(**code_file_attributes)

        __judge_code = open(os.path.join(self.working_dir, self.env_dir, code_file_obj.file_name), write_mode)
        __judge_code.write(code_file_obj.code)
        __judge_code.close()

        self.judge_solution_source = code_file_obj

        print(os.listdir(env_path))

    # noinspection DuplicatedCode
    def check_solution_event(self):
        self.prepare_environment()

        if self.__build__() != 0:
            self.solution.__update__('verdict', source.models.Verdict.BUILD_FAILED)
            self.solution.__update__('verdict_text', 'Ошибка компиляции')
            return

        _1 = BuildHandler.executable_file_name
        _2 = BuildHandler.build_log_file_name

        BuildHandler.executable_file_name = BuildHandler.executable_judge_file_name
        BuildHandler.build_log_file_name = BuildHandler.judge_build_log_file_name

        self.build_judge_solution(path=os.path.join(self.working_dir,
                                                    self.env_dir,
                                                    self.judge_solution_source.file_name),
                                  lang=self.judge_solution_source.language)

        BuildHandler.executable_file_name = _1
        BuildHandler.build_log_file_name = _2

        correct_tests_number: int = 0
        points: int = 0
        grading_system = None

        for test_number, test in enumerate(self.tests):
            input_file = open(os.path.join(self.env_dir, self.input_file_name), write_mode)
            input_file.write(test.content)
            input_file.close()

            print(f'Running on test {test_number + 1}')

            exec_code = self.__execute__(test_number=test_number + 1)
            print('execute code', exec_code)
            if exec_code > 0:
                self.solution.__update__('verdict', source.models.Verdict.RUNTIME_ERROR)
                self.solution.__update__('verdict_text', f'Ошибка исполнения на тесте {test_number + 1}')
                return
            elif exec_code < 0:
                self.solution.__update__('verdict', source.models.Verdict.TIME_LIMIT_ERROR)
                self.solution.__update__('verdict_text', f'Превышен лимит времени на тесте {test_number + 1}')
                return

            output_file = open(os.path.join(self.env_dir, self.output_file_name), read_mode)
            user_output = output_file.readlines()
            output_file.close()

            answer_type = self.__get_task_answer_type__()
            grading_system = self.__get_task_grading_system__()

            if answer_type == source.models.TaskAnswerType.CONSTANT_ANSWER:
                if self.is_constant_answer_valid(user_output=user_output, test_number=test_number):
                    correct_tests_number += 1
            elif answer_type == source.models.TaskAnswerType.VARIABLE_ANSWER:
                judge_verdict: int = self.is_variable_answer_valid(user_output=user_output, test_number=test_number)
                if grading_system == source.models.TaskGradingSystem.BINARY:
                    correct_tests_number += 1 if judge_verdict > 0 else 0
                elif grading_system == source.models.TaskGradingSystem.BINARY_FOR_EACH_TEST:
                    correct_tests_number += 1 if judge_verdict > 0 else 0
                elif grading_system == source.models.TaskGradingSystem.N_POINTS_FOR_EACH_TEST:
                    correct_tests_number += 1 if judge_verdict > 0 else 0
                    points += judge_verdict

        if grading_system == source.models.TaskGradingSystem.BINARY:
            self.solution.__update__('points', 1 if correct_tests_number == len(self.tests) else 0)
            if correct_tests_number == len(self.tests):
                self.solution.__update__('verdict', source.models.Verdict.CORRECT_SOLUTION)
                self.solution.__update__('verdict_text', f'Все тесты пройдены')
            else:
                self.solution.__update__('verdict', source.models.Verdict.WRONG_ANSWER)
        else:
            if correct_tests_number == len(self.tests):
                self.solution.__update__('verdict', source.models.Verdict.CORRECT_SOLUTION)
                self.solution.__update__('verdict_text', f'Все тесты пройдены')
            elif 0 < correct_tests_number < len(self.tests):
                self.solution.__update__('verdict', source.models.Verdict.PARTIAL_SOLUTION)
            elif correct_tests_number == 0:
                self.solution.__update__('verdict', source.models.Verdict.WRONG_ANSWER)
            if grading_system == source.models.TaskGradingSystem.BINARY_FOR_EACH_TEST:
                self.solution.__update__('points', correct_tests_number)
            else:
                self.solution.__update__('points', points)

    # noinspection DuplicatedCode
    def validate_task_event(self):

        self.solution.__update__('status', source.models.Status.IN_PROGRESS)
        self.prepare_environment()

        if self.__build__() != 0:
            self.solution.__update__('verdict', source.models.Verdict.BUILD_FAILED)
            self.solution.__update__('status', source.models.Status.CHECK_FAILED)
            return

        for test_number, test in enumerate(self.tests):
            input_file = open(os.path.join(self.env_dir, self.input_file_name), write_mode)
            input_file.write(test.content)
            input_file.close()

            print(f'Running on test {test_number + 1}')

            exec_code = self.__execute__(test_number=test_number)
            if exec_code > 0:
                self.solution.__update__('verdict', source.models.Verdict.RUNTIME_ERROR)
                self.solution.__update__('status', source.models.Status.CHECK_FAILED)
                return
            elif exec_code < 0:
                self.solution.__update__('verdict', source.models.Verdict.TIME_LIMIT_ERROR)
                self.solution.__update__('status', source.models.Status.CHECK_FAILED)
                return

            output_file = open(os.path.join(self.env_dir, self.output_file_name), read_mode)
            judge_output = output_file.read()
            output_file.close()

            test.__update__('right_answer', judge_output)

        self.solution.__update__('verdict', source.models.Verdict.CORRECT_SOLUTION)
        self.solution.__update__('status', source.models.Status.CHECK_SUCCESS)

    def __get_task_grading_system__(self):
        return source.models.Task.get_attribute('grading_system', self.solution.task_id)

    def __get_task_time_limit__(self):
        return source.models.Task.get_attribute('time_limit_seconds', self.solution.task_id)

    def __get_task_answer_type__(self):
        return source.models.Task.get_attribute('answer_type', self.solution.task_id)

    def __get_task_solution_file_id__(self):
        return source.models.Task.get_attribute('solution_file_id', self.solution.task_id)

    def build_judge_solution(self, path, lang):
        return self.__build__(path=path, lang=lang, )

    def __build__(self, **kwargs) -> 'Return code':
        """:param kwargs - can contain 'lang' and 'path' """
        print('lang', 0 if 'lang' not in kwargs else kwargs['lang'])
        if BuildHandler.get_execution_type(
                self.code_file.language
                if 'lang' not in kwargs else kwargs['lang']
        ) == source.models.CodeExecuteType.BUILD_AND_RUN:
            build_handler = BuildHandler(source_file_path=os.path.join(self.working_dir,
                                                                       self.env_dir,
                                                                       self.code_file.file_name
                                                                       if 'path' not in kwargs else kwargs['path']),
                                         language=self.code_file.language
                                         if 'lang' not in kwargs else kwargs['lang'])
            return build_handler.build()
        else:
            return 0

    def __execute__(self, test_number: int):
        execute_handler = ExecuteHandler(executable_file_path=self.get_execute_path(self.code_file.language),
                                         language=self.code_file.language,
                                         time_limit=self.__get_task_time_limit__(),
                                         test_number=test_number)

        return execute_handler.execute()

    def is_constant_answer_valid(self, user_output, test_number: int) -> bool:

        print('right ans:\n', TaskManager.string_to_array(
            self.tests[test_number].right_answer))
        print('user ans: \n', user_output)

        if TaskManager.handle_output_array(
                TaskManager.string_to_array(
                    self.tests[test_number].right_answer)) == TaskManager.handle_output_array(user_output):
            return True
        return False

    def is_variable_answer_valid(self, user_output, test_number: int) -> int or None:
        judge_execution_handler: ExecuteHandler = ExecuteHandler(
            executable_file_path=os.path.join(self.env_dir,
                                              BuildHandler.executable_judge_file_name),
            language=self.judge_solution_source.language,
            time_limit=2,
            test_number=test_number)
        user_out: str = open(f'{os.path.join(self.working_dir, self.env_dir, self.output_file_name)}', read_mode).read()
        test_content: str = self.tests[test_number].content

        print('user output:', user_out)

        judge_input_content: str = f'{test_content}\n{user_out}'
        print('judge input:\n=====\n', judge_input_content, '\n=====')

        __input = open(f'{os.path.join(self.working_dir, self.env_dir, self.input_file_name)}', write_mode)
        __input.write(judge_input_content)
        __input.close()

        if judge_execution_handler.execute() != 0:
            return 0

        output = open(os.path.join(self.working_dir, self.env_dir, self.output_file_name), read_mode)

        print('Judge output:', output.read())
        output.seek(0)

        return int(output.read())

    @staticmethod
    def string_to_array(string) -> List[str]:
        result: list = []
        for line in string.split('\n'):
            result.append(line)
        return result

    @staticmethod
    def string_drop_special_symbols(string: str) -> str:
        return string.replace('\n', '').replace('\r', '').replace('\t', '')

    @staticmethod
    def handle_output_array(array: List[str] or List[List[str]]) -> List[List[str]]:
        for i in range(len(array)):
            array[i] = TaskManager.string_drop_special_symbols(array[i]).split()
        return array

    # noinspection DuplicatedCode
    def get_execute_path(self, language: source.models.Language):
        execute_path = {
            source.models.Language.GNU_ASM: self.get_gnu_exe_path,
            source.models.Language.GNU_C99: self.get_gnu_exe_path,
            source.models.Language.GNU_C11: self.get_gnu_exe_path,
            source.models.Language.GNU_CXX_11: self.get_gnu_exe_path,
            source.models.Language.GNU_CXX_14: self.get_gnu_exe_path,
            source.models.Language.GNU_CXX_17: self.get_gnu_exe_path,
            source.models.Language.GNU_CXX_20: self.get_gnu_exe_path,
            source.models.Language.PYTHON_2_7: self.get_absolute_path,
            source.models.Language.PYTHON_3_9: self.get_absolute_path,
            source.models.Language.JAVA_8: self.get_class_name,
        }

        try:
            return execute_path[language]()
        except KeyError:
            return None

    def get_absolute_path(self):
        return os.path.join(self.working_dir, self.env_dir, self.code_file.file_name)

    def get_gnu_exe_path(self):
        return os.path.join(self.env_dir, BuildHandler.executable_file_name)

    def get_class_name(self):
        return self.code_file.file_name.split('.')[0]


class BuildHandler(object):
    executable_file_name: str = 'solution_executable'
    executable_judge_file_name: str = 'judge_solution_executable'
    build_log_file_name: str = 'build_log.out'
    judge_build_log_file_name: str = 'judge_build_log.out'

    def __init__(self, source_file_path: str, language: source.models.Language):
        print('build init')
        self.working_dir = os.getcwd()
        self.source_file = source_file_path
        self.language = language

    @staticmethod
    def get_execution_type(language: source.models.Language):
        print('get_execution_type')
        lang_info = {
            source.models.Language.GNU_ASM: source.models.CodeExecuteType.BUILD_AND_RUN,
            source.models.Language.GNU_C99: source.models.CodeExecuteType.BUILD_AND_RUN,
            source.models.Language.GNU_C11: source.models.CodeExecuteType.BUILD_AND_RUN,
            source.models.Language.GNU_CXX_11: source.models.CodeExecuteType.BUILD_AND_RUN,
            source.models.Language.GNU_CXX_14: source.models.CodeExecuteType.BUILD_AND_RUN,
            source.models.Language.GNU_CXX_17: source.models.CodeExecuteType.BUILD_AND_RUN,
            source.models.Language.GNU_CXX_20: source.models.CodeExecuteType.BUILD_AND_RUN,
            source.models.Language.PYTHON_2_7: source.models.CodeExecuteType.JUST_RUN,
            source.models.Language.PYTHON_3_9: source.models.CodeExecuteType.JUST_RUN,
            source.models.Language.JAVA_8: source.models.CodeExecuteType.BUILD_AND_RUN,
        }
        try:
            return lang_info[language]
        except KeyError:
            return None

    def build(self) -> 'Return code':
        print('build')

        build_command: str = self.get_build_command(source_path=self.source_file,
                                                    exe_path=os.path.join(
                                                        self.working_dir,
                                                        TaskManager.env_dir,
                                                        self.executable_file_name
                                                    ),
                                                    language=self.language)
        print()
        print(build_command)
        build_process = subprocess.Popen(
            build_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        try:
            build_process.wait(BUILD_SOURCE_MAX_TIME)
        except subprocess.TimeoutExpired:
            return 1

        log = open(os.path.join(self.working_dir,
                                TaskManager.env_dir,
                                self.build_log_file_name), 'a')
        log.write(build_process.communicate()[0].decode('utf-8'))
        log.write(build_process.communicate()[1].decode('utf-8'))
        log.close()

        print('code is', build_process.poll())

        return build_process.poll()

    def get_build_command(self, source_path: str,
                          exe_path: str,
                          language: source.models.Language):
        print('get_build_command')

        build_command = {
            source.models.Language.GNU_ASM: self.gbc_gnu_asm,
            source.models.Language.GNU_C99: self.gbc_gnu_gcc_c99,
            source.models.Language.GNU_C11: self.gbc_gnu_gcc_c11,
            source.models.Language.GNU_CXX_11: self.gbc_gnu_gxx_cxx11,
            source.models.Language.GNU_CXX_14: self.gbc_gnu_gxx_cxx14,
            source.models.Language.GNU_CXX_17: self.gbc_gnu_gxx_cxx17,
            source.models.Language.GNU_CXX_20: self.gbc_gnu_gxx_cxx20,
            source.models.Language.JAVA_8: self.gbc_java8,
        }

        try:
            return build_command[language](source_path=source_path,
                                           exe_path=exe_path,
                                           log=os.path.join(self.working_dir,
                                                            TaskManager.env_dir,
                                                            self.build_log_file_name))
        except KeyError:
            print('key error')
            return None

    @staticmethod
    def gbc_gnu_asm(source_path: str, exe_path: str, log: str):
        return f'gcc -s {source_path} -o {exe_path} -Wall -v -O3 -Ofast > {log}'

    @staticmethod
    def gbc_gnu_gcc_c99(source_path: str, exe_path: str, log: str):
        return f'gcc -std=c99 {source_path} -o {exe_path} -Wall -v -O3 -Ofast > {log}'

    @staticmethod
    def gbc_gnu_gcc_c11(source_path: str, exe_path: str, log: str):
        return f'gcc -std=c11 {source_path} -o {exe_path} -Wall -v -O3 -Ofast > {log}'

    @staticmethod
    def gbc_gnu_gxx_cxx11(source_path: str, exe_path: str, log: str):
        return f'g++ -std=c++11 {source_path} -o {exe_path} -Wall -v -O3 -Ofast > {log}'

    @staticmethod
    def gbc_gnu_gxx_cxx14(source_path: str, exe_path: str, log: str):
        return f'g++ -std=c++14 {source_path} -o {exe_path} -Wall -v -O3 -Ofast > {log}'

    @staticmethod
    def gbc_gnu_gxx_cxx17(source_path: str, exe_path: str, log: str):
        return f'g++ -std=c++17 {source_path} -o {exe_path} -Wall -v -O3 -Ofast > {log}'

    @staticmethod
    def gbc_gnu_gxx_cxx20(source_path: str, exe_path: str, log: str):
        return f'g++ -std=c++2a {source_path} -o {exe_path} -Wall -v -O3 -Ofast > {log}'

    @staticmethod
    def gbc_java8(source_path: str, exe_path: str, log: str):
        return f'javac -cp "{os.path.join(os.getcwd(), TaskManager.env_dir)}" {source_path} > {log}'


class ExecuteHandler(object):
    execute_log_file_name: str = 'execute_log.out'

    def __init__(self, executable_file_path: str,
                 language: source.models.Language,
                 time_limit: int,
                 test_number: int):
        self.executable_path = executable_file_path
        self.language = language
        self.time_limit = time_limit
        self.test_number = test_number

        try:
            self.executable_class = executable_file_path.split('/')[-1].split('.')[0]
            print(self.executable_class)
        except IndexError:
            pass

    def get_execute_command(self):
        execute_command: dict = {
            source.models.Language.GNU_ASM: self.gec_gnu_asm,
            source.models.Language.GNU_C99: self.gec_gnu_gcc_c99,
            source.models.Language.GNU_C11: self.gec_gnu_gcc_c11,
            source.models.Language.GNU_CXX_11: self.gec_gnu_gxx_cxx11,
            source.models.Language.GNU_CXX_14: self.gec_gnu_gxx_cxx14,
            source.models.Language.GNU_CXX_17: self.gec_gnu_gxx_cxx17,
            source.models.Language.GNU_CXX_20: self.gec_gnu_gxx_cxx20,
            source.models.Language.PYTHON_2_7: self.gec_python2,
            source.models.Language.PYTHON_3_9: self.gec_python3,
            source.models.Language.JAVA_8: self.gec_java8,
        }

        try:
            return execute_command[self.language](self.executable_path)
        except KeyError:
            return None

    @staticmethod
    def get_iostream_route():
        wd: str = os.getcwd()
        env: str = TaskManager.env_dir
        in_s: str = TaskManager.input_file_name
        out_s: str = TaskManager.output_file_name
        return f' < {os.path.join(wd, env, in_s)} > {os.path.join(wd, env, out_s)}'

    @staticmethod
    def gec_gnu_asm(executable_path: str):
        return f'.{executable_path}' + ExecuteHandler.get_iostream_route()

    @staticmethod
    def gec_gnu_gcc_c99(executable_path: str):
        return f'./{executable_path}' + ExecuteHandler.get_iostream_route()

    @staticmethod
    def gec_gnu_gcc_c11(executable_path: str):
        return f'./{executable_path}' + ExecuteHandler.get_iostream_route()

    @staticmethod
    def gec_gnu_gxx_cxx11(executable_path: str):
        return f'./{executable_path}' + ExecuteHandler.get_iostream_route()

    @staticmethod
    def gec_gnu_gxx_cxx14(executable_path: str):
        return f'./{executable_path}' + ExecuteHandler.get_iostream_route()

    @staticmethod
    def gec_gnu_gxx_cxx17(executable_path: str):
        return f'./{executable_path}' + ExecuteHandler.get_iostream_route()

    @staticmethod
    def gec_gnu_gxx_cxx20(executable_path: str):
        return f'./{executable_path}' + ExecuteHandler.get_iostream_route()

    @staticmethod
    def gec_python2(executable_path: str):
        return f'python2 {executable_path}' + ExecuteHandler.get_iostream_route()

    @staticmethod
    def gec_python3(executable_path: str):
        return f'python3 {executable_path}' + ExecuteHandler.get_iostream_route()

    @staticmethod
    def gec_java8(executable_path: str, **kwargs):
        env_dir_path: str = os.path.join(os.getcwd(), TaskManager.env_dir)
        return f'java -cp "{env_dir_path}/:{env_dir_path}/*" {executable_path}' + ExecuteHandler.get_iostream_route()

    def execute(self):
        execute_command: str = self.get_execute_command()

        print(execute_command)
        print(os.listdir(os.path.join(os.getcwd(), TaskManager.env_dir)))

        execute_process = subprocess.Popen(execute_command,
                                           shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)

        time_limit_expired: bool = False
        try:
            execute_process.wait(self.time_limit)
        except subprocess.TimeoutExpired:
            execute_process.terminate()
            execute_process.kill()
            print('Time limit exceeded!')
            print(execute_process.pid)
            return -1

        status = execute_process.poll()

        print('status is', status)
        execute_process.kill()
        print(time_limit_expired)
        stdout, stderr = execute_process.communicate()
        log = open(
            os.path.join(os.getcwd(),
                         TaskManager.env_dir,
                         f'test_{self.test_number}_' + self.execute_log_file_name), 'a')

        log.write(stdout.decode('utf-8'))
        log.write(stderr.decode('utf-8'))
        log.close()

        return status
