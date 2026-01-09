import hashlib
import os
from pathlib import Path

GIT_DIR = Path(".pika")
OBJECTS_DIR = GIT_DIR / "objects"


def init():
    os.makedirs(GIT_DIR)
    os.makedirs(OBJECTS_DIR)


def update_ref(ref, oid):
    ref_path = GIT_DIR / ref
    os.makedirs(os.path.dirname(ref_path), exist_ok=True)
    with open(ref_path, "w") as f:
        f.write(oid)


def get_ref(ref):
    ref_path = GIT_DIR / ref
    if os.path.isfile(ref_path):
        with open(ref_path) as f:
            return f.read().strip()


def iter_refs():
    refs = ["HEAD"]
    for root, _, filenames in os.walk(GIT_DIR / "refs"):
        root = os.path.relpath(root, GIT_DIR)
        refs.extend(str(Path(root) / name) for name in filenames)

    for refname in refs:
        yield refname, get_ref(refname)


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
