from typing import Tuple, Dict, Any


def sequence_to_dict(sequence, keys: Tuple[str]) -> Dict[(str, Any)]:
    result = dict()
    for value, key in zip(sequence, keys):
        try:
            result[key] = value
        except TypeError:
            pass
    return result
