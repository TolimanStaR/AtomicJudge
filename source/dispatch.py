import os
import psycopg2
import time
from multiprocessing import Queue
import threading
import datetime

from typing import List

from .config import NODE_NUMBER

from .models import SingletonMixin, Solution, Status, DataBase, CodeFile, Event, Test

from .service import sequence_to_dict

from .static import class_Solution_attributes
from .static import class_CodeFile_attributes
from .static import class_Test_attributes

from .task_manager import TaskManager


class Node(SingletonMixin):
    def __init__(self, **kwargs):
        node_number = os.getenv('NODE')
        if node_number is None:
            node_number = NODE_NUMBER

        self.node_number = node_number

        if 'node' in kwargs:
            self.node_number = kwargs['node']

        self.event_queue: Queue[Event] = Queue()

    def catch_new_solutions_from_db(self):
        db = DataBase()
        while True:
            sql = f'''SELECT *
                FROM management_solution
                WHERE management_solution.status='{Status.WAIT_FOR_CHECK}'
                AND management_solution.node={self.node_number};'''

            db.execute(sql)

            for solution_data in db.result():
                attributes = sequence_to_dict(solution_data, class_Solution_attributes)
                new_solution = Solution(**attributes)

                new_solution.__update__('status', Status.QUEUED)

                sql = f'''SELECT * 
                FROM management_codefile
                WHERE id={new_solution.get_code_file_id()};'''

                db.execute(sql)
                new_code_file = None

                for code_file_data in db.result():
                    attributes = sequence_to_dict(code_file_data, class_CodeFile_attributes)
                    new_code_file = CodeFile(**attributes)

                if new_code_file is not None:
                    new_code_file.set_solution(new_solution)

                new_solution.set_code_file(new_code_file)

                solution_task_id = new_solution.task_id

                sql = f'''SELECT *
                FROM management_test
                WHERE task_id={solution_task_id}'''

                db.execute(sql)
                tests: List[Test] = []

                for test_data in db.result():
                    attributes = sequence_to_dict(test_data, class_Test_attributes)
                    print(attributes)
                    new_test = Test(**attributes)
                    tests.append(new_test)

                new_event = Event(solution=new_solution, tests=tests)
                self.event_queue.put(new_event)

            print(self.event_queue.qsize())
            time.sleep(5)

    def handle_solutions_queue(self):
        while True:
            s = self.get_solution_from_queue()
            print(s)
            time.sleep(3)

    def get_solution_from_queue(self):
        return self.event_queue.get()
