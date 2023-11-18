import argparse
import os
from .core import create_doc_file


def main():
    parser = argparse.ArgumentParser(description="Generate Markdown documentation for a project directory.")
    parser.add_argument(
        "path",
        nargs="?",
        default=os.getcwd(),
        type=str,
        help="Path to the root of the project. Defaults to the current working directory.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=os.path.join(os.getcwd(), "reposcribe.md"),
        type=str,
        help="Path to save the generated Markdown file. Defaults to 'reposcribe.md' in the current working directory.",
    )
    args = parser.parse_args()

    create_doc_file(path=args.path, save_path=args.save_path)


if __name__ == "__main__":
    main()
