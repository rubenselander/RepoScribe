import os
from pathlib import Path
import re


DEFAULT_IGNORE_FILE_PATH = "reposcribe/ignore.txt"


def get_language_extensions() -> dict:
    """Returns a dictionary of file extensions and their corresponding language."""

    return {
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
        ".yml": "yaml",
        ".yaml": "yaml",
        ".md": None,
        # Add more mappings as needed
    }


def pattern_to_regex(pattern):
    """Convert a glob pattern to a regex pattern for matching, optimized for directory checks."""
    pattern = re.escape(pattern)  # Escape all regex characters
    pattern = pattern.replace(r"\*", ".*")  # Replace '*' with '.*'
    pattern = pattern.replace(r"\?", ".")  # Replace '?' with '.'
    if pattern.endswith("/"):  # Special handling for directory patterns
        pattern = pattern[:-1]  # Remove trailing slash for regex compatibility
    pattern += r"($|/)"  # Match end of string or directory separator
    return re.compile(pattern)


def load_ignore_patterns(file_path):
    """Load ignore patterns from a file and compile them into regex."""
    with open(file_path, "r") as file:
        patterns = [pattern_to_regex(line.strip()) for line in file if line.strip()]
    return patterns


def should_ignore_path(path, ignore_patterns):
    """Check if the given path matches any of the ignore patterns."""
    for pattern in ignore_patterns:
        if pattern.search(str(path)):
            return True
    return False


def find_files_with_extensions(
    extensions=[".py"], root_folder=None, ignore_patterns_file=DEFAULT_IGNORE_FILE_PATH
):
    """
    Find all file paths matching given extensions, excluding those that match patterns in ignore_patterns.txt.

    Parameters:
    - extensions: List of extensions to include.
    - root_folder: Root directory to search within. Defaults to the current working directory.
    - ignore_patterns_file: Path to a file containing patterns of files to ignore.

    Returns:
    - List of file paths matching the criteria.
    """
    if root_folder is None:
        root_folder = Path.cwd()
    else:
        root_folder = Path(root_folder)

    ignore_patterns = load_ignore_patterns(ignore_patterns_file)
    matching_files = []

    def search_directory(directory):
        for path in directory.iterdir():
            if should_ignore_path(path, ignore_patterns):
                continue  # Skip ignored paths
            if path.is_dir():
                search_directory(path)  # Recursively search directories
            elif any(path.suffix == ext for ext in extensions):
                matching_files.append(str(path))

    search_directory(root_folder)
    return matching_files


# def format_directory_structure(directory: str, ignore_patterns: list) -> str:
#     """Creates a structured representation of the directory tree, excluding ignored paths.

#     Args:
#         directory: The root directory path.
#         ignore_patterns: A list of patterns to ignore.

#     Returns:
#         A string representing the formatted directory tree structure.
#     """

#     def recurse_folder(current_dir: str, indent_level: int) -> str:
#         tree_str = ""
#         try:
#             for item in sorted(os.listdir(current_dir)):
#                 item_path = os.path.join(current_dir, item)
#                 if should_ignore(item_path, ignore_patterns):
#                     continue

#                 if os.path.isdir(item_path):
#                     tree_str += "    " * indent_level + f"- {item}/\n"
#                     tree_str += recurse_folder(item_path, indent_level + 1)
#                 else:
#                     tree_str += "    " * indent_level + f"- {item}\n"
#         except OSError as e:
#             tree_str += f"    " * indent_level + f"- Error accessing folder: {e}\n"
#         return tree_str

#     return recurse_folder(directory, 0)


def concatenate_files_to_markdown(files_to_include: list) -> str:
    """Concatenates all files in a directory and its subdirectories into a single Markdown string, excluding ignored paths.

    Args:
        directory: The root directory containing the files to concatenate.
        ignore_patterns: A list of patterns to ignore.

    Returns:
        A string containing the concatenated Markdown content of all files.
    """
    markdown_content = ""
    extensions_dict = get_language_extensions()

    for file_path in files_to_include:
        file_extension = os.path.splitext(file_path)[1]
        language = extensions_dict[file_extension]
        file_path_str = f"\n\nFile: {file_path}"
        markdown_content += file_path_str + "\n"
        markdown_content += f"```{language}\n"
        with open(file_path, "r", encoding="utf-8") as file:
            markdown_content += file.read() + "\n"
        markdown_content += "```\n\n"


def create_doc_file(
    root_path: str,
    save_path: str = None,
    include_file_tree: bool = True,
) -> str:
    """Generates a Markdown documentation for a project, optionally including the file tree, excluding paths specified in .gitignore.

    Args:
        root_path: The path to the root of the project, folder or file to document.
        format: The format of the output documentation (currently supports only 'md').
        save_path: The path where the output documentation should be saved (if provided).
        include_file_tree: Flag to include the file tree in the documentation.

    Returns:
        A string containing the generated documentation.
    """
    root_path = os.path.abspath(root_path)
    extensions_dict = get_language_extensions()
    extensions = list(extensions_dict.keys())
    all_file_paths = find_files_with_extensions(
        extensions=extensions,
        root_folder=root_path,
        ignore_patterns_file=DEFAULT_IGNORE_FILE_PATH,
    )

    if not save_path:
        save_path = os.path.join(root_path, "reposcribe.md")

    try:
        documentation = concatenate_files_to_markdown(all_file_paths)
        with open(save_path, "w", encoding="utf-8") as file:
            file.write(documentation)
        return documentation
    except Exception as e:
        raise Exception(f"Error generating documentation: {e}")
