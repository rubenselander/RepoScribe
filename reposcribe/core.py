import fnmatch
import os


DEFAULT_GITIGNORE_TXT_PATH = "reposcribe/ignore.txt"


def get_language_extension(file: str) -> str:
    """Determines the language extension for Markdown code blocks based on file extension.

    Args:
        file: The filename with extension.

    Returns:
        A string representing the programming language of the file for Markdown formatting.
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
        # Add more mappings as needed
    }
    return extensions.get(os.path.splitext(file)[1], "")


def read_gitignore(gitignore_path: str) -> list:
    """Reads a .gitignore file and returns a list of patterns to ignore.

    Args:
        gitignore_path: The path to the .gitignore file.

    Returns:
        A list of patterns to ignore.
    """
    ignore_patterns = []
    try:
        with open(gitignore_path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    ignore_patterns.append(line)
    except FileNotFoundError:
        pass
    return ignore_patterns


def should_ignore(path: str, ignore_patterns: list) -> bool:
    """Determines if a given path should be ignored based on .gitignore patterns.

    Args:
        path: The path to check.
        ignore_patterns: A list of patterns to ignore.

    Returns:
        True if the path should be ignored, False otherwise.
    """
    for pattern in ignore_patterns:
        # Clean the pattern by removing newline characters and leading/trailing spaces
        clean_pattern = pattern.strip()

        # Check if the pattern matches any part of the path
        if fnmatch.fnmatch(path, "*" + clean_pattern) or fnmatch.fnmatch(path, clean_pattern + "*"):
            return True
    return False


def format_directory_structure(directory: str, ignore_patterns: list) -> str:
    """Creates a structured representation of the directory tree, excluding ignored paths.

    Args:
        directory: The root directory path.
        ignore_patterns: A list of patterns to ignore.

    Returns:
        A string representing the formatted directory tree structure.
    """

    def recurse_folder(current_dir: str, indent_level: int) -> str:
        tree_str = ""
        try:
            for item in sorted(os.listdir(current_dir)):
                item_path = os.path.join(current_dir, item)
                if should_ignore(item_path, ignore_patterns):
                    continue

                if os.path.isdir(item_path):
                    tree_str += "    " * indent_level + f"- {item}/\n"
                    tree_str += recurse_folder(item_path, indent_level + 1)
                else:
                    tree_str += "    " * indent_level + f"- {item}\n"
        except OSError as e:
            tree_str += f"    " * indent_level + f"- Error accessing folder: {e}\n"
        return tree_str

    return recurse_folder(directory, 0)


def get_filtered_paths(directory: str, ignore_patterns: list) -> tuple[list[str], list[str]]:
    """Returns a tuple of two lists: the first containing all paths in the directory to include, the second containing all paths to ignore.

    Args:
        directory: The root directory path.
        ignore_patterns: A list of patterns to ignore.

    Returns:
        A tuple of two lists: the first containing all paths in the directory to include, the second containing all paths to ignore.
    """
    include_paths = []
    ignore_paths = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for dirname in dirnames:
            path = os.path.join(dirpath, dirname)
            if should_ignore(path, ignore_patterns):
                ignore_paths.append(path)
            else:
                include_paths.append(path)
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            if should_ignore(path, ignore_patterns):
                ignore_paths.append(path)
            else:
                include_paths.append(path)

    # def recurse_folder(directory: str, indent_level: int) -> str:
    #     try:
    #         for item in sorted(os.listdir(directory)):
    #             item_path = os.path.join(directory, item)
    #             if should_ignore(item_path, ignore_patterns):
    #                 continue

    #             if os.path.isdir(item_path):
    #                 tree_str += "    " * indent_level + f"- {item}/\n"
    #                 tree_str += recurse_folder(item_path, indent_level + 1)
    #             else:
    #                 tree_str += "    " * indent_level + f"- {item}\n"
    #     except OSError as e:
    #         tree_str += f"    " * indent_level + f"- Error accessing folder: {e}\n"
    #     return tree_str


def concatenate_files_to_markdown(directory: str, ignore_patterns: list) -> str:
    """Concatenates all files in a directory and its subdirectories into a single Markdown string, excluding ignored paths.

    Args:
        directory: The root directory containing the files to concatenate.
        ignore_patterns: A list of patterns to ignore.

    Returns:
        A string containing the concatenated Markdown content of all files.
    """
    markdown_content = ""
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if should_ignore(file_path, ignore_patterns):
                continue
            language = get_language_extension(file)
            markdown_content += f"\n\n## File: {file_path}\n"
            if language:
                markdown_content += f"```{language}\n"
            else:
                markdown_content += "```\n"
            try:
                with open(file_path, "r", encoding="utf-8") as infile:
                    markdown_content += infile.read()
            except Exception as e:
                markdown_content += f"Error reading file: {e}\n"
            markdown_content += "\n```"
    return markdown_content


def create_doc_file(
    root_path: str, format: str = "md", save_path: str = None, include_file_tree: bool = True
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
    gitignore_path = os.path.join(root_path, ".gitignore")
    if not os.path.exists(gitignore_path):
        gitignore_path = os.path.join(root_path, "reposcribe", DEFAULT_GITIGNORE_TXT_PATH)
    ignore_patterns = read_gitignore(gitignore_path)

    try:
        documentation = concatenate_files_to_markdown(root_path, ignore_patterns)
        if include_file_tree:
            file_tree = format_directory_structure(root_path, ignore_patterns)
            documentation += "\n\n## Directory Structure\n```\n" + file_tree + "```"

        if save_path:
            with open(save_path, "w", encoding="utf-8") as file:
                file.write(documentation)
        return documentation
    except Exception as e:
        raise Exception(f"Error generating documentation: {e}")
