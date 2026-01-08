import sys
import textwrap
from pathlib import Path
from typing import Optional

import typer

from . import base, data

app = typer.Typer()


@app.command()
def init():
    """Initialize a new pika repository."""
    data.init()
    print(f"Initialized empty pika repo in {Path.cwd() / data.GIT_DIR}")


@app.command()
def hash_object(file: str):
    """Hash a file and store it in the object database."""
    with open(file, "rb") as f:
        print(data.hash_object(f.read()))


@app.command()
def cat_file(object: str):
    """Print the contents of an object."""
    sys.stdout.flush()
    sys.stdout.buffer.write(data.get_object(object, expected=None))


@app.command()
def write_tree():
    """Write the current directory tree to the object database."""
    print(base.write_tree())


@app.command()
def read_tree(tree: str):
    """Read a tree object and restore files to the working directory."""
    print(base.read_tree(tree))


@app.command()
def commit(message: str = typer.Option(..., "--message", "-m")):
    """Create a new commit with the given message."""
    print(base.commit(message))


@app.command()
def log(oid: Optional[str] = None):
    """Show the commit log starting from the given commit or HEAD."""
    oid = oid or data.get_HEAD()
    while oid:
        commit = base.get_commit(oid)

        print(f"commit {oid}\n")
        print(textwrap.indent(commit.message, "    "))
        print("")

        oid = commit.parent


@app.command()
def checkout(oid: str):
    """Checkout a commit and update the working directory."""
    base.checkout(oid)


def main():
    app()
