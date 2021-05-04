import os
import psycopg2
import time
from multiprocessing import Queue
import threading
import datetime

from typing import List

from .config import *

from .models import SingletonMixin, Solution, Status, DataBase, CodeFile, Event, Test

from .service import sequence_to_dict

from .static import class_Solution_attributes
from .static import class_CodeFile_attributes
from .static import class_Test_attributes

from .task_manager import TaskManager


class Node(SingletonMixin):
    def __init__(self, **kwargs):
        node_number = os.getenv(NODE_NUMBER_ENVIRONMENT_VAR)
        if node_number is None:
            node_number = NODE_NUMBER

        self.node_number = node_number

        if 'node' in kwargs:
            self.node_number = kwargs['node']

        self.event_queue: Queue[Event] = Queue()

    def catch_new_solutions_from_db(self):
        db = DataBase()

        while True:
            db.execute(SQL_GET_SOLUTION, Status.WAIT_FOR_CHECK, self.node_number)

            for solution_data in db.result():
                attributes = sequence_to_dict(solution_data, class_Solution_attributes)
                new_solution = Solution(**attributes)
                new_solution.__update__(field='status', value=Status.QUEUED)

                db.execute(SQL_GET_CODE_FILE, new_solution.get_code_file_id())
                new_code_file = None

                for code_file_data in db.result():
                    attributes = sequence_to_dict(code_file_data, class_CodeFile_attributes)
                    new_code_file = CodeFile(**attributes)

                if new_code_file is not None:
                    new_code_file.set_solution(new_solution)

                new_solution.set_code_file(new_code_file)

                db.execute(SQL_GET_TESTS, new_solution.task_id)
                tests: List[Test] = []

                for test_data in db.result():
                    attributes = sequence_to_dict(test_data, class_Test_attributes)
                    new_test = Test(**attributes)
                    tests.append(new_test)

                new_event = Event(solution=new_solution, tests=tests)
                self.event_queue.put(new_event)

            print(self.event_queue.qsize())
            time.sleep(CATCH_SOLUTIONS_DELAY)

    def handle_solutions_queue(self):
        while True:
            s = self.get_solution_from_queue()
            print(s)
            time.sleep(3)

            # TODO: send every event to TaskManager

    def get_solution_from_queue(self):
        return self.event_queue.get()
