import os

import source.models


class TaskManager(object):
    env_dir: str = 'environment'

    def __init__(self, solution: source.models.Solution):
        self.working_dir = os.getcwd()

    def prepare_environment(self):
        if not os.path.exists(os.path.join(self.working_dir, self.env_dir)):
            os.mkdir(os.path.join(self.working_dir, self.env_dir))
        s = source.models.Solution()
        print(s)

    def check_solution(self):
        """"""

    def validate_task(self):
        """"""
