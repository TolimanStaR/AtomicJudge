import os

import source.models


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
        if not os.path.exists(env_path):
            os.mkdir(os.path.join(env_path))

        code_file: str = os.path.join(env_path, self.code_file.file_name)
        input_file: str = os.path.join(env_path, self.input_file_name)
        output_file: str = os.path.join(env_path, self.output_file_name)

    def __check_solution_event__(self):
        """"""

    def __validate_task_event__(self):
        """"""


class BuildCommand(object):
    pass


class ExecuteCommend(object):
    pass
