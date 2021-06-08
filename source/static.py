from typing import Tuple

class_Solution_attributes: Tuple = (
    'id',
    'author_id',
    'code_file_id',
    'created',
    'status',
    'verdict',
    'verdict_text',
    'task_id',
    'node',
    'event_type',
    'points',
)

class_CodeFile_attributes: Tuple = (
    'id',
    'file',
    'language',
    'code',
    'file_name',
)

class_Test_attributes: Tuple = (
    'id',
    'content',
    'right_answer',
    'task_id',
    'max_points',
)
read_mode: str = 'r'
write_mode: str = 'w'
