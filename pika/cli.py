import sys
import textwrap
from pathlib import Path

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
def cat_file(object: str | None = None):
    """Print the contents of an object."""
    object = base.get_oid(object or "@")
    sys.stdout.flush()
    sys.stdout.buffer.write(data.get_object(object, expected=None))


@app.command()
def write_tree():
    """Write the current directory tree to the object database."""
    print(base.write_tree())


@app.command()
def read_tree(tree: str | None = None):
    """Read a tree object and restore files to the working directory."""
    tree = base.get_oid(tree or "@")
    print(base.read_tree(tree))


@app.command()
def commit(message: str = typer.Option(..., "--message", "-m")):
    """Create a new commit with the given message."""
    print(base.commit(message))


@app.command()
def log(oid: str | None = None):
    """Show the commit log starting from the given commit or HEAD."""
    for oid in base.iter_commit_history({base.get_oid(oid or "@")}):
        commit = base.get_commit(oid)

        print(f"commit {oid}\n")
        print(textwrap.indent(commit.message, "    "))
        print("")


@app.command()
def checkout(oid: str | None = None):
    """Checkout a commit and update the working directory."""
    oid = base.get_oid(oid or "@")
    base.checkout(oid)


@app.command()
def tag(name: str, oid: str | None = None):
    """Tag a specific commit."""
    oid = base.get_oid(oid or "@")
    base.create_tag(name, oid)


@app.command()
def k():
    """Show the commit graph"""
    dot = "digraph commits {\n"

    oids = set()
    for refname, ref in data.iter_refs():
        dot += f'"{refname}" [shape=note]\n'
        dot += f'"{refname}" -> "{ref}"\n'
        oids.add(ref)

    for oid in base.iter_commits_and_parents(oids):
        commit = base.get_commit(oid)
        dot += f'"{oid}" [shape=box style=filled label="{oid[:10]}"]\n'
        if commit.parent:
            dot += f'"{oid}" -> "{commit.parent}"\n'

    dot += "}"
    print(dot)

@app.command()
def branch(name: str, start_point: str | None = None):
    start_point = base.get_oid(start_point or "@")
    base.create_branch(name, start_point)
    print (f'Branch {name} created at {start_point[:10]}')

def main():
    app()
