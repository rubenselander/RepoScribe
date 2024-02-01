from setuptools import setup, find_packages

setup(
    name="RepoScribe",
    version='0.2.1',
    author="Ruben Selander",
    author_email="info@nordicintel.com",
    description="A lightweight tool to compile project files and directories into a structured Markdown document",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/reversehobo/RepoScribe",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.10",  # Change as appropriate
    # install_requires=open("requirements.txt").read().splitlines(),
    entry_points={
        "console_scripts": [
            "reposcribe=reposcribe.cli:main",  # Assuming 'cli.py' contains the CLI interface
        ],
    },
)
