import os


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


def format_directory_structure(directory: str) -> str:
    """Creates a structured representation of the directory tree.

    Args:
        directory: The root directory path.

    Returns:
        A string representing the formatted directory tree structure.
    """

    def recurse_folder(current_dir: str, indent_level: int) -> str:
        tree_str = ""
        try:
            for item in sorted(os.listdir(current_dir)):
                item_path = os.path.join(current_dir, item)
                if os.path.isdir(item_path):
                    tree_str += "    " * indent_level + f"- {item}/\n"
                    tree_str += recurse_folder(item_path, indent_level + 1)
                else:
                    tree_str += "    " * indent_level + f"- {item}\n"
        except OSError as e:
            tree_str += f"    " * indent_level + f"- Error accessing folder: {e}\n"
        return tree_str

    return recurse_folder(directory, 0)


def concatenate_files_to_markdown(directory: str) -> str:
    """Concatenates all files in a directory and its subdirectories into a single Markdown string.

    Args:
        directory: The root directory containing the files to concatenate.

    Returns:
        A string containing the concatenated Markdown content of all files.
    """
    markdown_content = ""
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
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
    """Generates a Markdown documentation for a project, optionally including the file tree.

    Args:
        root_path: The path to the root of the project, folder or file to document.
        format: The format of the output documentation (currently supports only 'md').
        save_path: The path where the output documentation should be saved (if provided).
        include_file_tree: Flag to include the file tree in the documentation.

    Returns:
        A string containing the generated documentation.
    """
    try:
        documentation = concatenate_files_to_markdown(root_path)
        if include_file_tree:
            file_tree = format_directory_structure(root_path)
            documentation += "\n\n## Directory Structure\n```\n" + file_tree + "```"

        if save_path:
            with open(save_path, "w", encoding="utf-8") as file:
                file.write(documentation)
        return documentation
    except Exception as e:
        raise Exception(f"Error generating documentation: {e}")
