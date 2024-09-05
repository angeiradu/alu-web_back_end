#!/usr/bin/env python3
"""define function to_kv"""


from ast import Tuple
from ctypes import Union


def to_kv(K: str, v: Union[int, float]) -> Tuple[str, float]:
    """return a tuple"""
    return (K, v * v)
