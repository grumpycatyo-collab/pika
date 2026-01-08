import os
import hashlib
from pathlib import Path

GIT_DIR = Path(".pika")
OBJECTS_DIR = GIT_DIR / "objects"

def init():
    os.makedirs(GIT_DIR)
    os.makedirs(OBJECTS_DIR)


def hash_object(data, type_='blob'):
    obj = type_.encode() + b'\x00' + data # \x00 - object header separator
    oid = hashlib.sha1(obj).hexdigest()
    with open(OBJECTS_DIR / oid, 'wb') as out:
        out.write(obj)
    return oid

def get_object(oid, expected='blob'):
    with open (OBJECTS_DIR / oid, 'rb') as f:
        obj = f.read()
    
    type_, _, content = obj.partition (b'\x00')
    type_ = type_.decode ()

    if expected is not None and type_ != expected:
        raise ValueError(f'Expected {expected}, got {type_}')
    return content