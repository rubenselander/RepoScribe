import os
from pathlib import Path
import re


DEFAULT_IGNORE_FILE_PATH = "ignore.txt"


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


def get_ignore_patterns():
    """Get ignore patterns compiled into regex."""
    pattern_lines = [
        "__pycache__/",
        "*.py[cod]",
        "*$py.class",
        "*.so",
        ".Python",
        "build/",
        "develop-eggs/",
        "dist/",
        "downloads/",
        "eggs/",
        ".eggs/",
        "lib/",
        "lib64/",
        "parts/",
        "sdist/",
        "var/",
        "wheels/",
        "share/python-wheels/",
        "*.egg-info/",
        ".installed.cfg",
        "*.egg",
        "MANIFEST",
        "*.manifest",
        "*.spec",
        "pip-log.txt",
        "pip-delete-this-directory.txt",
        "htmlcov/",
        ".tox/",
        ".nox/",
        ".coverage",
        ".coverage.*",
        ".cache",
        "nosetests.xml",
        "coverage.xml",
        "*.cover",
        "*.py,cover",
        ".hypothesis/",
        ".pytest_cache/",
        "cover/",
        "*.mo",
        "*.pot",
        "*.log",
        "local_settings.py",
        "db.sqlite3",
        "db.sqlite3-journal",
        "instance/",
        ".webassets-cache",
        ".scrapy",
        "docs/_build/",
        ".pybuilder/",
        "target/",
        ".ipynb_checkpoints",
        "profile_default/",
        "ipython_config.py",
        ".pdm.toml",
        "__pypackages__/",
        "celerybeat-schedule",
        "celerybeat.pid",
        "*.sage.py",
        ".env",
        ".venv",
        "env/",
        "venv/",
        "ENV/",
        "env.bak/",
        "venv.bak/",
        ".spyderproject",
        ".spyproject",
        ".ropeproject",
        "/site",
        ".mypy_cache/",
        ".dmypy.json",
        "dmypy.json",
        ".pyre/",
        ".pytype/",
        "cython_debug/",
        "ignore_patterns.txt",
        "*.gitignore",
        ".gitignore",
        ".venv",
        "venv",
        "*test*",
        "*tests*",
        "*ignore*",
        "*ignore/*",
        "ignore.txt",
        "reposcribe.md",
        "*reposcribe*",
        "RepoScribe.md",
    ]
    patterns = [pattern_to_regex(line) for line in pattern_lines]
    return patterns


def should_ignore_path(path, ignore_patterns):
    """Check if the given path matches any of the ignore patterns."""
    for pattern in ignore_patterns:
        if pattern.search(str(path)):
            return True
    return False


def find_files_with_extensions(extensions=[".py"], root_folder=None):
    """
    Find all file paths matching given extensions, excluding those that match patterns in ignore_patterns.txt.

    Parameters:
    - extensions: List of extensions to include.
    - root_folder: Root directory to search within. Defaults to the current working directory.


    Returns:
    - List of file paths matching the criteria.
    """
    if root_folder is None:
        root_folder = Path.cwd()
    else:
        root_folder = Path(root_folder)

    ignore_patterns = get_ignore_patterns()
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
