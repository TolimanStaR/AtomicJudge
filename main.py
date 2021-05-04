import argparse
import threading

from source.dispatch import Node
from source.models import Solution

from source.task_manager import TaskManager


def main():
    node = Node()

    get_solutions_thread = threading.Thread(target=node.catch_new_solutions_from_db)
    send_solutions_to_check_thread = threading.Thread(target=node.handle_solutions_queue)

    get_solutions_thread.start()
    send_solutions_to_check_thread.start()

    # t = TaskManager(Solution())
    # t.prepare_environment()


if __name__ == '__main__':
    main()
