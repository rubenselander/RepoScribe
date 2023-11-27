import fnmatch
import os
import pathspec


DEFAULT_GITIGNORE_TXT_PATH = "reposcribe/ignore.txt"
SPEC = None


def read_gitignore(gitignore_path: str = None) -> list:
    """Reads a .gitignore or .txt file and returns a the file contents as a string with lines containing comments or
    empty lines removed.

    Args:
        gitignore_path: The path to the .gitignore file.

    Returns:
        A list of patterns to ignore.
    """
    if not gitignore_path:
        gitignore_path = DEFAULT_GITIGNORE_TXT_PATH

    ignore_patterns = []
    try:
        with open(gitignore_path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    ignore_patterns.append(line)
    except FileNotFoundError:
        if gitignore_path != DEFAULT_GITIGNORE_TXT_PATH:
            print(
                f"Warning: Unable to find .gitignore file at {gitignore_path}. Using default .gitignore file."
            )
            return read_gitignore()
        else:
            raise FileNotFoundError(f"Unable to find .gitignore file at {gitignore_path}.")

    output_str = "\n".join(ignore_patterns)
    return output_str


def get_all_file_paths(root_directory: str) -> list:
    """Returns a list of all file paths in the root directory.

    Args:
        root_directory: The root directory path.

    Returns:
        A list of all file paths in the root directory.
    """
    all_file_paths = [
        os.path.join(root, file)
        for root, _, files in os.walk(root_directory)
        for file in files
        if os.path.isfile(os.path.join(root, file)) and os.path.exists(os.path.join(root, file))
    ]
    return all_file_paths


def is_code_file(file_path: str) -> bool:
    """Determines if a file is a code file based on its extension.

    Args:
        file_path: The path to the file.

    Returns:
        True if the file is a code file, False otherwise.
    """
    extensions = {
        ".py": "python",
        ".js": "javascript",
        ".html": "html",
        ".css": "css",
        ".java": "java",
        ".cpp": "cpp",
        ".c": "c",
        ".sh": "bash",
        ".R": "r",
        ".cs": "csharp",
        ".go": "go",
        ".php": "php",
        ".rb": "ruby",
        ".rs": "rust",
        ".sql": "sql",
        ".swift": "swift",
        ".ts": "typescript",
        ".vb": "vb",
        ".xml": "xml",
        ".yml": "yaml",
        "yaml": "yaml",
        # Add more mappings as needed
    }
    is_code_file = True if extensions.get(os.path.splitext(file_path)[1], None) else False
    return is_code_file


def get_filtered_paths(all_file_paths: list, gitignore_path: str) -> list:
    """Returns a list of all file paths in the root directory that are not excluded by the .gitignore file.

    Args:
        all_file_paths: A list of all file paths in the root directory.
        gitignore_path: The path to the .gitignore file.

    Returns:
        A list of all file paths in the root directory that are not excluded by the .gitignore file.
    """

    spec_text = read_gitignore(gitignore_path)
    spec = pathspec.GitIgnoreSpec.from_lines(spec_text.splitlines())

    not_in_gitignore = spec.match_files(files=all_file_paths, negate=True)
    return not_in_gitignore
