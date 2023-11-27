from reposcribe.core import *
import os
import fnmatch
from termcolor import cprint


def test_read_gitignore(gitignore_path: str, verbose=True) -> list:
    if verbose:
        print("test_read_gitignore")
    ignore_patterns = read_gitignore(gitignore_path)

    if verbose:
        print("type(ignore_patterns): ", type(ignore_patterns))
        print("type(ignore_patterns[0]): ", type(ignore_patterns[0]))

        print("ignore_patterns: ")
        for pattern in ignore_patterns:
            print(pattern)
    return ignore_patterns


def test_should_ignore() -> bool:
    paths = [
        ".env",
        ".gitignore",
        "README.md",
        "setup.py",
        "tests/test_core.py",
        ".venv/lib/python3.8/site-packages/",
    ]
    patterns = ["*.env", "*.venv", "env/", "venv/", "ENV/", "env.bak/", "venv.bak/"]
    for path in paths:
        ignore_path = should_ignore(path, patterns)
        print(f"path: {path}. \nshould_ignore: {ignore_path}")
        print()


def get_paths():
    directory = os.getcwd()
    paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            paths.append(file_path)

    return paths


with open("paths.txt", "w") as file:
    for path in get_paths():
        file.write(path + "\n")
