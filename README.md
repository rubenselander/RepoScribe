
# RepoScribe

RepoScribe is a basic, lightweight tool for compiling your codebase and directory structure into a structured Markdown document. It is designed to enrich Large Language Models (LLMs) with project-specific context, but it's also highly effective for straightforward navigation and review of code projects or folders.

## Installation

To install RepoScribe, simply use pip:

```bash
pip install RepoScribe
```

RepoScribe is designed to be lightweight and self-contained, with no external dependencies. This makes it easy to integrate into your projects without worrying about additional package requirements.

## Usage

### In the Terminal

RepoScribe can be used directly from your command line. You can run it in your project's root directory to create a Markdown file of the entire project:

```bash
reposcribe
```

This command will generate a `reposcribe.md` file in the current directory. If you want to specify the root directory of your project and the output file location, you can do so as follows:

```bash
reposcribe /path/to/project /path/to/output.md
```

### In a Python File

You can also use RepoScribe programmatically in your Python scripts. Here's a simple usage example:

```python
from reposcribe import create_doc_file

# Generate documentation for the project
project_doc = create_doc_file(root_path='/path/to/project', save_path='/path/to/output.md')

# The `project_doc` variable now contains the Markdown content
print(project_doc)
```

## Features

- Compile entire projects into a single Markdown document.
- Include a detailed file and directory structure.
- Simple and intuitive command-line interface.
- Flexible usage - run in your project's root directory with no arguments or specify paths as needed.

Download the latest version of RepoScribe [here](https://pypi.org/project/RepoScribe/).
