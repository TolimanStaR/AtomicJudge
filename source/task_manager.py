import os
import shutil
import subprocess

import source.models

from .static import *

from .config import BUILD_SOURCE_MAX_TIME


class TaskManager(object):
    env_dir: str = 'environment'
    input_file_name: str = 'input.in'
    output_file_name: str = 'output.out'

    def __init__(self, event: source.models.Event):
        self.working_dir = os.getcwd()
        self.solution = event.solution
        self.code_file: source.models.CodeFile = event.code_file
        self.tests = event.tests

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

        print(os.listdir(env_path))

    def check_solution_event(self):
        self.prepare_environment()
        if self.__build__() != 0:
            self.solution.__update__('verdict', source.models.Verdict.BUILD_FAILED)

        if self.__execute__() != 0:
            self.solution.__update__('verdict', source.models.Verdict.RUNTIME_ERROR)

        # build -> for t in test -> check test

    def validate_task_event(self):
        self.prepare_environment()

    def __build__(self) -> 'Return code':
        if BuildHandler.get_execution_type(
                self.code_file.language
        ) == source.models.CodeExecuteType.BUILD_AND_RUN:
            build_handler = BuildHandler(source_file_path=os.path.join(self.working_dir,
                                                                       self.env_dir,
                                                                       self.code_file.file_name),
                                         language=self.code_file.language)
            return build_handler.build()
        return -1

    def __execute__(self):
        execute_handler = ExecuteHandler(self.get_execute_path(self.code_file.language), self.code_file.language)

        """
        todo: get execute path. for c/c++ it is ~/env/{a.exe}, 
        for python it is just source and for java it is class name
        """

    def get_execute_path(self, language: source.models.Language):
        execute_path = {

        }

        try:
            return execute_path[language]
        except KeyError:
            return None


class BuildHandler(object):
    executable_file_name: str = 'solution_executable'
    build_log_file_name: str = 'build_log.out'

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
                 time_limit: int):
        self.executable_path = executable_file_path
        self.language = language
        self.time_limit = time_limit

        # Only for java:
        # may be unused:

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
            return execute_command[self.language](self.executable_path, exe_class=self.executable_class)
        except KeyError:
            return None

    @staticmethod
    def get_iostream_route():
        wd: str = os.getcwd()
        env: str = TaskManager.env_dir
        in_s: str = TaskManager.input_file_name
        out_s: str = TaskManager.input_file_name
        return f' < {os.path.join(wd, env, in_s)} > {os.path.join(wd, env, out_s)}'

    @staticmethod
    def gec_gnu_asm(executable_path: str):
        return f'.{executable_path}' + ExecuteHandler.get_iostream_route()

    @staticmethod
    def gec_gnu_gcc_c99(executable_path: str):
        return f'.{executable_path}' + ExecuteHandler.get_iostream_route()

    @staticmethod
    def gec_gnu_gcc_c11(executable_path: str):
        return f'.{executable_path}' + ExecuteHandler.get_iostream_route()

    @staticmethod
    def gec_gnu_gxx_cxx11(executable_path: str):
        return f'.{executable_path}' + ExecuteHandler.get_iostream_route()

    @staticmethod
    def gec_gnu_gxx_cxx14(executable_path: str):
        return f'.{executable_path}' + ExecuteHandler.get_iostream_route()

    @staticmethod
    def gec_gnu_gxx_cxx17(executable_path: str):
        return f'.{executable_path}' + ExecuteHandler.get_iostream_route()

    @staticmethod
    def gec_gnu_gxx_cxx20(executable_path: str):
        return f'.{executable_path}' + ExecuteHandler.get_iostream_route()

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

        execute_process = subprocess.Popen(execute_command,
                                           shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)

        try:
            execute_process.wait(self.time_limit)
        except subprocess.TimeoutExpired:
            execute_process.kill()
            pass  # todo: add return code

        status = execute_process.poll()

        execute_process.kill()
        stdout, stderr = execute_process.communicate()
        log = open(os.path.join(os.getcwd(), TaskManager.env_dir, self.execute_log_file_name), 'a')

        log.write(stdout.decode('utf-8'))
        log.write(stderr.decode('utf-8'))

        return status
