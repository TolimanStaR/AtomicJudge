import argparse
import psycopg2
import os
import time
import threading

from source.dispatch import Node


def main():
    node = Node()
    node.catch_new_solutions_from_db()


if __name__ == '__main__':
    main()
