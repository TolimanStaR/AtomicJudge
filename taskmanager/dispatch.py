from .models import Task, SolutionCase, TestCase, Status, Language, LanguageType, language_extension
import multiprocessing
import subprocess
import time
import os


class TaskManager(object):
    env_dir: str = 'environment'
    solution_input: str = 'solution_input'
    solution_output: str = 'solution_output'
    solution_source: str = 'solution_source'
    solution_executable: str = 'solution_executable'
    judge_solution_source: str = 'judge_solution_source'
    judge_solution_executable: str = 'judge_solution_executable'
    judge_output: str = 'judge_output'

    def __init__(self, solution: SolutionCase):
        self.solution: SolutionCase = solution
        self.working_dir: str = os.getcwd()

    def check_solution(self):
        self.prepare_env_dir()

    def prepare_env_dir(self):
        if not os.path.exists(os.path.join(self.working_dir, self.env_dir)):
            os.mkdir(os.path.join(self.working_dir, self.env_dir))
        else:
            os.system(f'rm -rf {os.path.join(self.working_dir, self.env_dir, "*")}')

        try:
            ext: str = language_extension[self.solution.language]
        except KeyError:
            pass

        user_solution_path: str = os.path.join(self.working_dir, self.env_dir, f'{self.solution.file_name}.{ext}')
        os.system(f'touch {user_solution_path}')
        os.system(f'chmod 722 {user_solution_path}')
        os.system(f'echo {self.solution.code} > {user_solution_path}')

        if self.solution.language_type == LanguageType.COMPILE:
            command: str = self.get_build_command(self.solution.file_name, self.solution.language)
            code: int = self.__build__(user_solution_path, command)

    def run_all_tests(self):
        pass

    def run_test(self, test: TestCase):
        pass

    def get_build_command(self, file_name: str, language: str) -> str:
        return BuildSource.gbc(self=BuildSource(),
                               source=file_name,
                               executable=self.solution_executable,
                               path=self.working_dir,
                               language=language)

    def get_execute_command(self, file_name: str, language: str) -> str:
        pass

    def run_judge_solution(self, task: Task):
        pass

    @staticmethod
    def __build__(file_name: str, command: str) -> int:
        # subprocess run -> and build
        pass

    @staticmethod
    def __execute__(file_name: str, command: str, input_file: str, output_file: str) -> int:
        pass


class NodeManager(object):
    node_env_var_name: str = 'NODE'

    def __init__(self):
        self.node = 0
        self.queue = multiprocessing.Queue()

    def catch_new_solutions_from_db(self):
        while True:
            time.sleep(10)
            new_solutions: list = SolutionCase.objects.filter(status=Status.NOT_CHECKED, serving_note=self.node)
            for solution in new_solutions:
                solution.status = Status.IN_PROCESS
                solution.save()
                self.queue.put(solution)

    def send_new_solutions_to_judgement(self):
        while not self.queue.empty():
            manager = TaskManager(self.queue.get())
            manager.check_solution()
            manager.solution.save()

    def update_node_id(self, node: int):
        self.node = node
        os.system(f'{self.node_env_var_name}=\'{node}\'')
        os.system(f'export {self.node_env_var_name}')


class BuildSource(object):
    def __init__(self):
        self.build_function: dict = {
            Language.GNU_ASM: self.gbc_gnu_asm,
            Language.GNU_C_99: self.gbc_gnu_c_99,
            Language.GNU_C_11: self.gbc_gnu_c_11,
            Language.GNU_CXX_11: self.gbc_gnu_cxx_11,
            Language.GNU_CXX_14: self.gbc_gnu_cxx_14,
            Language.GNU_CXX_17: self.gbc_gnu_cxx_17,
            Language.PYTHON_2_7: self.gbc_python_2_7,
            Language.PYTHON_3_8: self.gbc_python_3_8,
            Language.PYPY: self.gbc_pypy,
            Language.JAVA_11: self.gbc_java_11,
            Language.RUBY_2_7: self.gbc_ruby,
            Language.KOTLIN: self.gbc_kotlin,
            Language.GOLANG: self.gbc_golang,
            Language.CSHARP: self.gbc_csharp,
            Language.BASH: self.gbc_bash,
        }

    def gbc(self, source: str, executable: str, path: str, language: str):
        try:
            return self.build_function[language](source, executable, path)
        except KeyError:
            print('No lang detected')

    @staticmethod
    def gbc_gnu_asm(source: str, executable: str, path: str) -> str:
        return f'gcc -s {os.path.join(path, source)} -o {os.path.join(path, executable)} --stack,128000000'

    @staticmethod
    def gbc_gnu_c_99(source: str, executable: str, path: str) -> str:
        return f'gcc {os.path.join(path, source)} -o {os.path.join(path, executable)} ' \
               f'-std=c99 -O3 -Ofast -Os --stack,128000000'

    @staticmethod
    def gbc_gnu_c_11(source: str, executable: str, path: str) -> str:
        return f'gcc {os.path.join(path, source)} -o {os.path.join(path, executable)} ' \
               f'-std=c11 -O3 -Ofast -Os --stack,128000000'

    @staticmethod
    def gbc_gnu_cxx_11(source: str, executable: str, path: str) -> str:
        return f'g++ {os.path.join(path, source)} -o {os.path.join(path, executable)} ' \
               f'-std=c++11 -O3 -Ofast -Os --stack,128000000'

    @staticmethod
    def gbc_gnu_cxx_14(source: str, executable: str, path: str) -> str:
        return f'g++ {os.path.join(path, source)} -o {os.path.join(path, executable)} ' \
               f'-std=c++14 -O3 -Ofast -Os --stack,128000000'

    @staticmethod
    def gbc_gnu_cxx_17(source: str, executable: str, path: str) -> str:
        return f'g++ {os.path.join(path, source)} -o {os.path.join(path, executable)} ' \
               f'-std=c++17 -O3 -Ofast -Os --stack,128000000'

    @staticmethod
    def gbc_python_2_7() -> str:
        return str()

    @staticmethod
    def gbc_python_3_8() -> str:
        return str()

    @staticmethod
    def gbc_pypy() -> str:
        return str()

    @staticmethod
    def gbc_java_11(source: str, path: str) -> str:
        return f'javac {os.path.join(path, source)}'

    @staticmethod
    def gbc_ruby() -> str:
        return str()

    @staticmethod
    def gbc_kotlin() -> str:
        return str()

    @staticmethod
    def gbc_golang() -> str:
        return str()

    @staticmethod
    def gbc_csharp() -> str:
        return str()

    @staticmethod
    def gbc_bash() -> str:
        return str()


class ExecuteSolution(object):
    pass
