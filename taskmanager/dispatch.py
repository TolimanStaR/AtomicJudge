from .models import Task, SolutionCase, TestCase, Status, Language
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

    def check_solution(self):
        self.prepare_env_dir()

    def prepare_env_dir(self):
        working_dir: str = os.getcwd()
        if not os.path.exists(os.path.join(working_dir, self.env_dir)):
            os.mkdir(os.path.join(working_dir, self.env_dir))
        else:
            os.system(f'rm -rf {os.path.join(working_dir, self.env_dir, "*")}')

    def run_all_tests(self):
        pass

    def run_test(self, test: TestCase):
        pass

    def get_build_command(self, file_name: str, language: Language) -> str:
        pass

    def get_execute_command(self, file_name: str, language: Language) -> str:
        pass

    @staticmethod
    def __build__(file_name: str, command: str, input_file: str, output_file: str):
        pass

    @staticmethod
    def __execute__(file_name: str, command: str, input_file: str, output_file: str) -> int:
        pass


class NodeManager(object):

    def __init__(self):
        # TODO: add global variable "NODE"
        self.node = 0
        self.queue = multiprocessing.Queue()

    def catch_new_solutions(self):
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
        os.system(f'NODE=\'{node}\'')
        os.system('export NODE')
