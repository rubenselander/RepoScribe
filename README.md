# RepoScribe
RepoScribe is a basic, lightweight tool for compiling your codebase and directory structure into a structured Markdown document. It is designed to enrich Large Language Models (LLMs) with project-specific context, but it's also highly effective for straightforward navigation and review of code projects or folders. The python package is self-contained, with no external dependencies.


<div style="text-align: center;">
  <img src="reposcribe_logo.png" alt="The kindly helper" style="max-width: 30%; height: auto; display: block; margin: 0 auto;">
</div>


## Installation

To install RepoScribe, simply use pip:

```bash
pip install RepoScribe
```

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

- **File Type Filters**: Specify a list of file extensions or file names to include or exclude from the documentation.

## Planned Features

- **Multiple Output Formats**: Allow exporting documentation to formats like HTML, PDF, or a Word document.
- **Code Syntax Highlighting**: Integrate syntax highlighting in the generated Markdown for better readability of code snippets.
- **Documenting Non-Code Files**: Include a structured summary of non-code files (like images, text files) in the project.
- **GitHub Integration**: Generate documentation by specifying a public GitHub repository.
- **Dependency Graphs**: Generate visual dependency graphs for the project, showing how different files and modules are interconnected.

