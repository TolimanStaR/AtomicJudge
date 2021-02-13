from .models import Task, SolutionCase, TestCase, Status, Language
import multiprocessing
import time


class TaskManager(object):
    def __init__(self, solution: SolutionCase):
        self.solution: SolutionCase = solution

    def check_solution(self):
        pass

    def build_executable(self, language: Language):
        pass

    def run_all_tests(self):
        pass

    def run_test(self, test: TestCase):
        pass

    def get_build_command(self):
        pass

    def execute_command(self):
        pass


class QueueManager(object):

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
        pass

    def update_node(self):
        pass
