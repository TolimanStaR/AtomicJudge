import os
import psycopg2

from .config import NODE_NUMBER


class Node(object):

    def __init__(self):
        node_number = os.getenv('NODE')
        if node_number is None:
            node_number = NODE_NUMBER

        self.node_number = node_number

    def catch_new_solutions_from_db():
        pass

    def handle_solutions_queue():
        pass
