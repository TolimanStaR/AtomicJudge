import os
import psycopg2
import time
from multiprocessing import Queue
import threading
import datetime

from .config import NODE_NUMBER

from .models import SingletonMixin, Solution, Status

from .service import sequence_to_dict

from .static import class_Solution_attributes


class DataBase(SingletonMixin):
    def __init__(self):
        passwd = os.getenv('COURSEWORK2_DB_PASSWORD')
        self.connection = psycopg2.connect(dbname='age-of-python',
                                           user='postgres',
                                           password=f'{passwd}',
                                           host='185.139.70.166')
        self.cursor = self.connection.cursor()

    def execute(self, sql_request, *params):
        self.cursor.execute(sql_request, params)

    def result(self):
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()

    def close_connection(self):
        self.connection.close()

    def __str__(self):
        pass


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
                WHERE management_solution.status='{Status.WAIT_FOR_CHECK}';'''

            db.execute(sql)

            for solution_data in db.result():
                attributes = sequence_to_dict(solution_data, class_Solution_attributes)
                new_solution = Solution(**attributes)
                self.solutions_queue.put(new_solution)

            time.sleep(5)

    def handle_solutions_queue(self):
        pass
