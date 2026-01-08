import hashlib
import os
from pathlib import Path

GIT_DIR = Path(".pika")
OBJECTS_DIR = GIT_DIR / "objects"
HEAD_DIR = GIT_DIR / "HEAD"


def init():
    os.makedirs(GIT_DIR)
    os.makedirs(OBJECTS_DIR)


def set_HEAD(oid):
    with open(HEAD_DIR, "w") as f:
        f.write(oid)


def get_HEAD():
    if os.path.isfile(HEAD_DIR):
        with open(HEAD_DIR) as f:
            return f.read().strip()


def hash_object(data, type_="blob"):
    obj = type_.encode() + b"\x00" + data  # \x00 - object header separator
    oid = hashlib.sha1(obj).hexdigest()
    with open(OBJECTS_DIR / oid, "wb") as out:
        out.write(obj)
    return oid


def get_object(oid, expected="blob"):
    with open(OBJECTS_DIR / oid, "rb") as f:
        obj = f.read()

    type_, _, content = obj.partition(b"\x00")
    type_ = type_.decode()

    if expected is not None and type_ != expected:
        raise ValueError(f"Expected {expected}, got {type_}")
    return content
