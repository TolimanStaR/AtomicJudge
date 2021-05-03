import os
import psycopg2
import time
from multiprocessing import Queue
import threading
import datetime

from .config import NODE_NUMBER

from .models import SingletonMixin, Solution, Status, DataBase, CodeFile

from .service import sequence_to_dict

from .static import class_Solution_attributes
from .static import class_CodeFile_attributes


class Node(SingletonMixin):
    def __init__(self, **kwargs):
        node_number = os.getenv('NODE')
        if node_number is None:
            node_number = NODE_NUMBER

        self.node_number = node_number

        if 'node' in kwargs:
            self.node_number = kwargs['node']

        self.solutions_queue: Queue[Solution] = Queue()

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
                self.solutions_queue.put(new_solution)
                new_solution.__update__('status', Status.QUEUED)
                print(new_solution)

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

            time.sleep(5)

    def handle_solutions_queue(self):
        pass
