

## File: C:\Users\Admin\Documents\RepoScribe\.env
```
PYPI_TOKEN = "pypi-AgEIcHlwaS5vcmcCJDgxNmI1YTQ1LWIwNjEtNGQ2Ny1iNmM3LTc2NjMyYTE1Mjk0YQACKlszLCIzMWY4N2I5NS00ZDQyLTQwN2YtYjc5Zi1kN2Q1ZWI5OTM3OWQiXQAABiC11ObmM1PMbd7bFKTgmfiGOWT203oLRq0YQ8i4gXB_jw"
```

## File: C:\Users\Admin\Documents\RepoScribe\.gitignore
```
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/#use-with-ide
.pdm.toml

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/



#deployment scripts
deploy.py
```

## File: C:\Users\Admin\Documents\RepoScribe\deploy.py
```python
import os
import re
import shutil
import subprocess
from dotenv import load_dotenv

load_dotenv()


def increment_version(version: str) -> str:
    """Increment the patch number of a semantic version string."""
    major, minor, patch = map(int, version.split("."))
    return f"{major}.{minor}.{patch + 1}"


def update_setup_py_version(new_version: str):
    """Update the version number in setup.py."""
    with open("setup.py", "r") as file:
        content = file.read()

    # Match both single and double quotes
    content = re.sub(r"version=['\"]([\d\.]+)['\"]", f"version='{new_version}'", content)

    with open("setup.py", "w") as file:
        file.write(content)


def deploy_package():
    """Automates the process of updating a Python package from GitHub to PyPI."""
    pypi_token = os.getenv("PYPI_TOKEN")
    if not pypi_token:
        raise ValueError("PyPI token not found in .env file")

    # Increment version number
    with open("setup.py", "r") as file:
        setup_content = file.read()
        current_version_match = re.search(r"version=['\"]([\d\.]+)['\"]", setup_content)

        if not current_version_match:
            raise ValueError("Unable to find the current version in setup.py")

        current_version = current_version_match.group(1)
        new_version = increment_version(current_version)

    update_setup_py_version(new_version)
    print(f"Updated version to {new_version}")

    # Clear out old distributions
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    os.makedirs("dist", exist_ok=True)

    # Pull latest changes from GitHub
    subprocess.run(["git", "pull"], check=True)

    # Build the package
    subprocess.run(["python", "setup.py", "sdist", "bdist_wheel"], check=True)

    # Upload to PyPI
    subprocess.run(
        [
            "twine",
            "upload",
            "dist/*",
            "--repository",
            "pypi",
            "--non-interactive",
            "--username",
            "__token__",
            "--password",
            pypi_token,
        ],
        check=True,
    )


if __name__ == "__main__":
    deploy_package()

```

## File: C:\Users\Admin\Documents\RepoScribe\LICENSE
```
MIT License

Copyright (c) 2023 Reversehobo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```

## File: C:\Users\Admin\Documents\RepoScribe\README.md
```
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

## Planned Features

- **Multiple Output Formats**: Allow exporting documentation to formats like HTML, PDF, or a Word document.
- **Code Syntax Highlighting**: Integrate syntax highlighting in the generated Markdown for better readability of code snippets.
- **Documenting Non-Code Files**: Include a structured summary of non-code files (like images, text files) in the project.
- **GitHub Integration**: Generate documentation by specifying a public GitHub repository.
- **File Type Filters**: Specify a list of file extensions or file names to include or exclude from the documentation.
- **Dependency Graphs**: Generate visual dependency graphs for the project, showing how different files and modules are interconnected.

```

## File: C:\Users\Admin\Documents\RepoScribe\reposcribe_logo.png
```
Error reading file: 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\setup.py
```python
from setuptools import setup, find_packages

setup(
    name="RepoScribe",
    version='0.1.5',
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
    python_requires=">=3.8",  # Change as appropriate
    entry_points={
        "console_scripts": [
            "reposcribe=reposcribe.cli:main",  # Assuming 'cli.py' contains the CLI interface
        ],
    },
)

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\COMMIT_EDITMSG
```
new version

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\config
```
[core]
	repositoryformatversion = 0
	filemode = false
	bare = false
	logallrefupdates = true
	symlinks = false
	ignorecase = true
[remote "origin"]
	url = https://github.com/Reversehobo/RepoScribe.git
	fetch = +refs/heads/*:refs/remotes/origin/*
[branch "main"]
	remote = origin
	merge = refs/heads/main

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\description
```
Unnamed repository; edit this file 'description' to name the repository.

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\FETCH_HEAD
```
c391f1a646519f97c3f9810e87096df7066739a1		branch 'main' of https://github.com/Reversehobo/RepoScribe

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\HEAD
```
ref: refs/heads/main

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\index
```
Error reading file: 'utf-8' codec can't decode byte 0xe0 in position 14: invalid continuation byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\ORIG_HEAD
```
c391f1a646519f97c3f9810e87096df7066739a1

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\packed-refs
```
# pack-refs with: peeled fully-peeled sorted 
6cd69b61f11659d4b01448d2465428b70ef4a211 refs/remotes/origin/main

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\hooks\applypatch-msg.sample
```
#!/bin/sh
#
# An example hook script to check the commit log message taken by
# applypatch from an e-mail message.
#
# The hook should exit with non-zero status after issuing an
# appropriate message if it wants to stop the commit.  The hook is
# allowed to edit the commit message file.
#
# To enable this hook, rename this file to "applypatch-msg".

. git-sh-setup
commitmsg="$(git rev-parse --git-path hooks/commit-msg)"
test -x "$commitmsg" && exec "$commitmsg" ${1+"$@"}
:

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\hooks\commit-msg.sample
```
#!/bin/sh
#
# An example hook script to check the commit log message.
# Called by "git commit" with one argument, the name of the file
# that has the commit message.  The hook should exit with non-zero
# status after issuing an appropriate message if it wants to stop the
# commit.  The hook is allowed to edit the commit message file.
#
# To enable this hook, rename this file to "commit-msg".

# Uncomment the below to add a Signed-off-by line to the message.
# Doing this in a hook is a bad idea in general, but the prepare-commit-msg
# hook is more suited to it.
#
# SOB=$(git var GIT_AUTHOR_IDENT | sed -n 's/^\(.*>\).*$/Signed-off-by: \1/p')
# grep -qs "^$SOB" "$1" || echo "$SOB" >> "$1"

# This example catches duplicate Signed-off-by lines.

test "" = "$(grep '^Signed-off-by: ' "$1" |
	 sort | uniq -c | sed -e '/^[ 	]*1[ 	]/d')" || {
	echo >&2 Duplicate Signed-off-by lines.
	exit 1
}

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\hooks\fsmonitor-watchman.sample
```
#!/usr/bin/perl

use strict;
use warnings;
use IPC::Open2;

# An example hook script to integrate Watchman
# (https://facebook.github.io/watchman/) with git to speed up detecting
# new and modified files.
#
# The hook is passed a version (currently 2) and last update token
# formatted as a string and outputs to stdout a new update token and
# all files that have been modified since the update token. Paths must
# be relative to the root of the working tree and separated by a single NUL.
#
# To enable this hook, rename this file to "query-watchman" and set
# 'git config core.fsmonitor .git/hooks/query-watchman'
#
my ($version, $last_update_token) = @ARGV;

# Uncomment for debugging
# print STDERR "$0 $version $last_update_token\n";

# Check the hook interface version
if ($version ne 2) {
	die "Unsupported query-fsmonitor hook version '$version'.\n" .
	    "Falling back to scanning...\n";
}

my $git_work_tree = get_working_dir();

my $retry = 1;

my $json_pkg;
eval {
	require JSON::XS;
	$json_pkg = "JSON::XS";
	1;
} or do {
	require JSON::PP;
	$json_pkg = "JSON::PP";
};

launch_watchman();

sub launch_watchman {
	my $o = watchman_query();
	if (is_work_tree_watched($o)) {
		output_result($o->{clock}, @{$o->{files}});
	}
}

sub output_result {
	my ($clockid, @files) = @_;

	# Uncomment for debugging watchman output
	# open (my $fh, ">", ".git/watchman-output.out");
	# binmode $fh, ":utf8";
	# print $fh "$clockid\n@files\n";
	# close $fh;

	binmode STDOUT, ":utf8";
	print $clockid;
	print "\0";
	local $, = "\0";
	print @files;
}

sub watchman_clock {
	my $response = qx/watchman clock "$git_work_tree"/;
	die "Failed to get clock id on '$git_work_tree'.\n" .
		"Falling back to scanning...\n" if $? != 0;

	return $json_pkg->new->utf8->decode($response);
}

sub watchman_query {
	my $pid = open2(\*CHLD_OUT, \*CHLD_IN, 'watchman -j --no-pretty')
	or die "open2() failed: $!\n" .
	"Falling back to scanning...\n";

	# In the query expression below we're asking for names of files that
	# changed since $last_update_token but not from the .git folder.
	#
	# To accomplish this, we're using the "since" generator to use the
	# recency index to select candidate nodes and "fields" to limit the
	# output to file names only. Then we're using the "expression" term to
	# further constrain the results.
	my $last_update_line = "";
	if (substr($last_update_token, 0, 1) eq "c") {
		$last_update_token = "\"$last_update_token\"";
		$last_update_line = qq[\n"since": $last_update_token,];
	}
	my $query = <<"	END";
		["query", "$git_work_tree", {$last_update_line
			"fields": ["name"],
			"expression": ["not", ["dirname", ".git"]]
		}]
	END

	# Uncomment for debugging the watchman query
	# open (my $fh, ">", ".git/watchman-query.json");
	# print $fh $query;
	# close $fh;

	print CHLD_IN $query;
	close CHLD_IN;
	my $response = do {local $/; <CHLD_OUT>};

	# Uncomment for debugging the watch response
	# open ($fh, ">", ".git/watchman-response.json");
	# print $fh $response;
	# close $fh;

	die "Watchman: command returned no output.\n" .
	"Falling back to scanning...\n" if $response eq "";
	die "Watchman: command returned invalid output: $response\n" .
	"Falling back to scanning...\n" unless $response =~ /^\{/;

	return $json_pkg->new->utf8->decode($response);
}

sub is_work_tree_watched {
	my ($output) = @_;
	my $error = $output->{error};
	if ($retry > 0 and $error and $error =~ m/unable to resolve root .* directory (.*) is not watched/) {
		$retry--;
		my $response = qx/watchman watch "$git_work_tree"/;
		die "Failed to make watchman watch '$git_work_tree'.\n" .
		    "Falling back to scanning...\n" if $? != 0;
		$output = $json_pkg->new->utf8->decode($response);
		$error = $output->{error};
		die "Watchman: $error.\n" .
		"Falling back to scanning...\n" if $error;

		# Uncomment for debugging watchman output
		# open (my $fh, ">", ".git/watchman-output.out");
		# close $fh;

		# Watchman will always return all files on the first query so
		# return the fast "everything is dirty" flag to git and do the
		# Watchman query just to get it over with now so we won't pay
		# the cost in git to look up each individual file.
		my $o = watchman_clock();
		$error = $output->{error};

		die "Watchman: $error.\n" .
		"Falling back to scanning...\n" if $error;

		output_result($o->{clock}, ("/"));
		$last_update_token = $o->{clock};

		eval { launch_watchman() };
		return 0;
	}

	die "Watchman: $error.\n" .
	"Falling back to scanning...\n" if $error;

	return 1;
}

sub get_working_dir {
	my $working_dir;
	if ($^O =~ 'msys' || $^O =~ 'cygwin') {
		$working_dir = Win32::GetCwd();
		$working_dir =~ tr/\\/\//;
	} else {
		require Cwd;
		$working_dir = Cwd::cwd();
	}

	return $working_dir;
}

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\hooks\post-update.sample
```
#!/bin/sh
#
# An example hook script to prepare a packed repository for use over
# dumb transports.
#
# To enable this hook, rename this file to "post-update".

exec git update-server-info

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\hooks\pre-applypatch.sample
```
#!/bin/sh
#
# An example hook script to verify what is about to be committed
# by applypatch from an e-mail message.
#
# The hook should exit with non-zero status after issuing an
# appropriate message if it wants to stop the commit.
#
# To enable this hook, rename this file to "pre-applypatch".

. git-sh-setup
precommit="$(git rev-parse --git-path hooks/pre-commit)"
test -x "$precommit" && exec "$precommit" ${1+"$@"}
:

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\hooks\pre-commit.sample
```
#!/bin/sh
#
# An example hook script to verify what is about to be committed.
# Called by "git commit" with no arguments.  The hook should
# exit with non-zero status after issuing an appropriate message if
# it wants to stop the commit.
#
# To enable this hook, rename this file to "pre-commit".

if git rev-parse --verify HEAD >/dev/null 2>&1
then
	against=HEAD
else
	# Initial commit: diff against an empty tree object
	against=$(git hash-object -t tree /dev/null)
fi

# If you want to allow non-ASCII filenames set this variable to true.
allownonascii=$(git config --type=bool hooks.allownonascii)

# Redirect output to stderr.
exec 1>&2

# Cross platform projects tend to avoid non-ASCII filenames; prevent
# them from being added to the repository. We exploit the fact that the
# printable range starts at the space character and ends with tilde.
if [ "$allownonascii" != "true" ] &&
	# Note that the use of brackets around a tr range is ok here, (it's
	# even required, for portability to Solaris 10's /usr/bin/tr), since
	# the square bracket bytes happen to fall in the designated range.
	test $(git diff --cached --name-only --diff-filter=A -z $against |
	  LC_ALL=C tr -d '[ -~]\0' | wc -c) != 0
then
	cat <<\EOF
Error: Attempt to add a non-ASCII file name.

This can cause problems if you want to work with people on other platforms.

To be portable it is advisable to rename the file.

If you know what you are doing you can disable this check using:

  git config hooks.allownonascii true
EOF
	exit 1
fi

# If there are whitespace errors, print the offending file names and fail.
exec git diff-index --check --cached $against --

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\hooks\pre-merge-commit.sample
```
#!/bin/sh
#
# An example hook script to verify what is about to be committed.
# Called by "git merge" with no arguments.  The hook should
# exit with non-zero status after issuing an appropriate message to
# stderr if it wants to stop the merge commit.
#
# To enable this hook, rename this file to "pre-merge-commit".

. git-sh-setup
test -x "$GIT_DIR/hooks/pre-commit" &&
        exec "$GIT_DIR/hooks/pre-commit"
:

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\hooks\pre-push.sample
```
#!/bin/sh

# An example hook script to verify what is about to be pushed.  Called by "git
# push" after it has checked the remote status, but before anything has been
# pushed.  If this script exits with a non-zero status nothing will be pushed.
#
# This hook is called with the following parameters:
#
# $1 -- Name of the remote to which the push is being done
# $2 -- URL to which the push is being done
#
# If pushing without using a named remote those arguments will be equal.
#
# Information about the commits which are being pushed is supplied as lines to
# the standard input in the form:
#
#   <local ref> <local oid> <remote ref> <remote oid>
#
# This sample shows how to prevent push of commits where the log message starts
# with "WIP" (work in progress).

remote="$1"
url="$2"

zero=$(git hash-object --stdin </dev/null | tr '[0-9a-f]' '0')

while read local_ref local_oid remote_ref remote_oid
do
	if test "$local_oid" = "$zero"
	then
		# Handle delete
		:
	else
		if test "$remote_oid" = "$zero"
		then
			# New branch, examine all commits
			range="$local_oid"
		else
			# Update to existing branch, examine new commits
			range="$remote_oid..$local_oid"
		fi

		# Check for WIP commit
		commit=$(git rev-list -n 1 --grep '^WIP' "$range")
		if test -n "$commit"
		then
			echo >&2 "Found WIP commit in $local_ref, not pushing"
			exit 1
		fi
	fi
done

exit 0

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\hooks\pre-rebase.sample
```
#!/bin/sh
#
# Copyright (c) 2006, 2008 Junio C Hamano
#
# The "pre-rebase" hook is run just before "git rebase" starts doing
# its job, and can prevent the command from running by exiting with
# non-zero status.
#
# The hook is called with the following parameters:
#
# $1 -- the upstream the series was forked from.
# $2 -- the branch being rebased (or empty when rebasing the current branch).
#
# This sample shows how to prevent topic branches that are already
# merged to 'next' branch from getting rebased, because allowing it
# would result in rebasing already published history.

publish=next
basebranch="$1"
if test "$#" = 2
then
	topic="refs/heads/$2"
else
	topic=`git symbolic-ref HEAD` ||
	exit 0 ;# we do not interrupt rebasing detached HEAD
fi

case "$topic" in
refs/heads/??/*)
	;;
*)
	exit 0 ;# we do not interrupt others.
	;;
esac

# Now we are dealing with a topic branch being rebased
# on top of master.  Is it OK to rebase it?

# Does the topic really exist?
git show-ref -q "$topic" || {
	echo >&2 "No such branch $topic"
	exit 1
}

# Is topic fully merged to master?
not_in_master=`git rev-list --pretty=oneline ^master "$topic"`
if test -z "$not_in_master"
then
	echo >&2 "$topic is fully merged to master; better remove it."
	exit 1 ;# we could allow it, but there is no point.
fi

# Is topic ever merged to next?  If so you should not be rebasing it.
only_next_1=`git rev-list ^master "^$topic" ${publish} | sort`
only_next_2=`git rev-list ^master           ${publish} | sort`
if test "$only_next_1" = "$only_next_2"
then
	not_in_topic=`git rev-list "^$topic" master`
	if test -z "$not_in_topic"
	then
		echo >&2 "$topic is already up to date with master"
		exit 1 ;# we could allow it, but there is no point.
	else
		exit 0
	fi
else
	not_in_next=`git rev-list --pretty=oneline ^${publish} "$topic"`
	/usr/bin/perl -e '
		my $topic = $ARGV[0];
		my $msg = "* $topic has commits already merged to public branch:\n";
		my (%not_in_next) = map {
			/^([0-9a-f]+) /;
			($1 => 1);
		} split(/\n/, $ARGV[1]);
		for my $elem (map {
				/^([0-9a-f]+) (.*)$/;
				[$1 => $2];
			} split(/\n/, $ARGV[2])) {
			if (!exists $not_in_next{$elem->[0]}) {
				if ($msg) {
					print STDERR $msg;
					undef $msg;
				}
				print STDERR " $elem->[1]\n";
			}
		}
	' "$topic" "$not_in_next" "$not_in_master"
	exit 1
fi

<<\DOC_END

This sample hook safeguards topic branches that have been
published from being rewound.

The workflow assumed here is:

 * Once a topic branch forks from "master", "master" is never
   merged into it again (either directly or indirectly).

 * Once a topic branch is fully cooked and merged into "master",
   it is deleted.  If you need to build on top of it to correct
   earlier mistakes, a new topic branch is created by forking at
   the tip of the "master".  This is not strictly necessary, but
   it makes it easier to keep your history simple.

 * Whenever you need to test or publish your changes to topic
   branches, merge them into "next" branch.

The script, being an example, hardcodes the publish branch name
to be "next", but it is trivial to make it configurable via
$GIT_DIR/config mechanism.

With this workflow, you would want to know:

(1) ... if a topic branch has ever been merged to "next".  Young
    topic branches can have stupid mistakes you would rather
    clean up before publishing, and things that have not been
    merged into other branches can be easily rebased without
    affecting other people.  But once it is published, you would
    not want to rewind it.

(2) ... if a topic branch has been fully merged to "master".
    Then you can delete it.  More importantly, you should not
    build on top of it -- other people may already want to
    change things related to the topic as patches against your
    "master", so if you need further changes, it is better to
    fork the topic (perhaps with the same name) afresh from the
    tip of "master".

Let's look at this example:

		   o---o---o---o---o---o---o---o---o---o "next"
		  /       /           /           /
		 /   a---a---b A     /           /
		/   /               /           /
	       /   /   c---c---c---c B         /
	      /   /   /             \         /
	     /   /   /   b---b C     \       /
	    /   /   /   /             \     /
    ---o---o---o---o---o---o---o---o---o---o---o "master"


A, B and C are topic branches.

 * A has one fix since it was merged up to "next".

 * B has finished.  It has been fully merged up to "master" and "next",
   and is ready to be deleted.

 * C has not merged to "next" at all.

We would want to allow C to be rebased, refuse A, and encourage
B to be deleted.

To compute (1):

	git rev-list ^master ^topic next
	git rev-list ^master        next

	if these match, topic has not merged in next at all.

To compute (2):

	git rev-list master..topic

	if this is empty, it is fully merged to "master".

DOC_END

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\hooks\pre-receive.sample
```
#!/bin/sh
#
# An example hook script to make use of push options.
# The example simply echoes all push options that start with 'echoback='
# and rejects all pushes when the "reject" push option is used.
#
# To enable this hook, rename this file to "pre-receive".

if test -n "$GIT_PUSH_OPTION_COUNT"
then
	i=0
	while test "$i" -lt "$GIT_PUSH_OPTION_COUNT"
	do
		eval "value=\$GIT_PUSH_OPTION_$i"
		case "$value" in
		echoback=*)
			echo "echo from the pre-receive-hook: ${value#*=}" >&2
			;;
		reject)
			exit 1
		esac
		i=$((i + 1))
	done
fi

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\hooks\prepare-commit-msg.sample
```
#!/bin/sh
#
# An example hook script to prepare the commit log message.
# Called by "git commit" with the name of the file that has the
# commit message, followed by the description of the commit
# message's source.  The hook's purpose is to edit the commit
# message file.  If the hook fails with a non-zero status,
# the commit is aborted.
#
# To enable this hook, rename this file to "prepare-commit-msg".

# This hook includes three examples. The first one removes the
# "# Please enter the commit message..." help message.
#
# The second includes the output of "git diff --name-status -r"
# into the message, just before the "git status" output.  It is
# commented because it doesn't cope with --amend or with squashed
# commits.
#
# The third example adds a Signed-off-by line to the message, that can
# still be edited.  This is rarely a good idea.

COMMIT_MSG_FILE=$1
COMMIT_SOURCE=$2
SHA1=$3

/usr/bin/perl -i.bak -ne 'print unless(m/^. Please enter the commit message/..m/^#$/)' "$COMMIT_MSG_FILE"

# case "$COMMIT_SOURCE,$SHA1" in
#  ,|template,)
#    /usr/bin/perl -i.bak -pe '
#       print "\n" . `git diff --cached --name-status -r`
# 	 if /^#/ && $first++ == 0' "$COMMIT_MSG_FILE" ;;
#  *) ;;
# esac

# SOB=$(git var GIT_COMMITTER_IDENT | sed -n 's/^\(.*>\).*$/Signed-off-by: \1/p')
# git interpret-trailers --in-place --trailer "$SOB" "$COMMIT_MSG_FILE"
# if test -z "$COMMIT_SOURCE"
# then
#   /usr/bin/perl -i.bak -pe 'print "\n" if !$first_line++' "$COMMIT_MSG_FILE"
# fi

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\hooks\push-to-checkout.sample
```
#!/bin/sh

# An example hook script to update a checked-out tree on a git push.
#
# This hook is invoked by git-receive-pack(1) when it reacts to git
# push and updates reference(s) in its repository, and when the push
# tries to update the branch that is currently checked out and the
# receive.denyCurrentBranch configuration variable is set to
# updateInstead.
#
# By default, such a push is refused if the working tree and the index
# of the remote repository has any difference from the currently
# checked out commit; when both the working tree and the index match
# the current commit, they are updated to match the newly pushed tip
# of the branch. This hook is to be used to override the default
# behaviour; however the code below reimplements the default behaviour
# as a starting point for convenient modification.
#
# The hook receives the commit with which the tip of the current
# branch is going to be updated:
commit=$1

# It can exit with a non-zero status to refuse the push (when it does
# so, it must not modify the index or the working tree).
die () {
	echo >&2 "$*"
	exit 1
}

# Or it can make any necessary changes to the working tree and to the
# index to bring them to the desired state when the tip of the current
# branch is updated to the new commit, and exit with a zero status.
#
# For example, the hook can simply run git read-tree -u -m HEAD "$1"
# in order to emulate git fetch that is run in the reverse direction
# with git push, as the two-tree form of git read-tree -u -m is
# essentially the same as git switch or git checkout that switches
# branches while keeping the local changes in the working tree that do
# not interfere with the difference between the branches.

# The below is a more-or-less exact translation to shell of the C code
# for the default behaviour for git's push-to-checkout hook defined in
# the push_to_deploy() function in builtin/receive-pack.c.
#
# Note that the hook will be executed from the repository directory,
# not from the working tree, so if you want to perform operations on
# the working tree, you will have to adapt your code accordingly, e.g.
# by adding "cd .." or using relative paths.

if ! git update-index -q --ignore-submodules --refresh
then
	die "Up-to-date check failed"
fi

if ! git diff-files --quiet --ignore-submodules --
then
	die "Working directory has unstaged changes"
fi

# This is a rough translation of:
#
#   head_has_history() ? "HEAD" : EMPTY_TREE_SHA1_HEX
if git cat-file -e HEAD 2>/dev/null
then
	head=HEAD
else
	head=$(git hash-object -t tree --stdin </dev/null)
fi

if ! git diff-index --quiet --cached --ignore-submodules $head --
then
	die "Working directory has staged changes"
fi

if ! git read-tree -u -m "$commit"
then
	die "Could not update working tree to new HEAD"
fi

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\hooks\sendemail-validate.sample
```
#!/bin/sh

# An example hook script to validate a patch (and/or patch series) before
# sending it via email.
#
# The hook should exit with non-zero status after issuing an appropriate
# message if it wants to prevent the email(s) from being sent.
#
# To enable this hook, rename this file to "sendemail-validate".
#
# By default, it will only check that the patch(es) can be applied on top of
# the default upstream branch without conflicts in a secondary worktree. After
# validation (successful or not) of the last patch of a series, the worktree
# will be deleted.
#
# The following config variables can be set to change the default remote and
# remote ref that are used to apply the patches against:
#
#   sendemail.validateRemote (default: origin)
#   sendemail.validateRemoteRef (default: HEAD)
#
# Replace the TODO placeholders with appropriate checks according to your
# needs.

validate_cover_letter () {
	file="$1"
	# TODO: Replace with appropriate checks (e.g. spell checking).
	true
}

validate_patch () {
	file="$1"
	# Ensure that the patch applies without conflicts.
	git am -3 "$file" || return
	# TODO: Replace with appropriate checks for this patch
	# (e.g. checkpatch.pl).
	true
}

validate_series () {
	# TODO: Replace with appropriate checks for the whole series
	# (e.g. quick build, coding style checks, etc.).
	true
}

# main -------------------------------------------------------------------------

if test "$GIT_SENDEMAIL_FILE_COUNTER" = 1
then
	remote=$(git config --default origin --get sendemail.validateRemote) &&
	ref=$(git config --default HEAD --get sendemail.validateRemoteRef) &&
	worktree=$(mktemp --tmpdir -d sendemail-validate.XXXXXXX) &&
	git worktree add -fd --checkout "$worktree" "refs/remotes/$remote/$ref" &&
	git config --replace-all sendemail.validateWorktree "$worktree"
else
	worktree=$(git config --get sendemail.validateWorktree)
fi || {
	echo "sendemail-validate: error: failed to prepare worktree" >&2
	exit 1
}

unset GIT_DIR GIT_WORK_TREE
cd "$worktree" &&

if grep -q "^diff --git " "$1"
then
	validate_patch "$1"
else
	validate_cover_letter "$1"
fi &&

if test "$GIT_SENDEMAIL_FILE_COUNTER" = "$GIT_SENDEMAIL_FILE_TOTAL"
then
	git config --unset-all sendemail.validateWorktree &&
	trap 'git worktree remove -ff "$worktree"' EXIT &&
	validate_series
fi

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\hooks\update.sample
```
#!/bin/sh
#
# An example hook script to block unannotated tags from entering.
# Called by "git receive-pack" with arguments: refname sha1-old sha1-new
#
# To enable this hook, rename this file to "update".
#
# Config
# ------
# hooks.allowunannotated
#   This boolean sets whether unannotated tags will be allowed into the
#   repository.  By default they won't be.
# hooks.allowdeletetag
#   This boolean sets whether deleting tags will be allowed in the
#   repository.  By default they won't be.
# hooks.allowmodifytag
#   This boolean sets whether a tag may be modified after creation. By default
#   it won't be.
# hooks.allowdeletebranch
#   This boolean sets whether deleting branches will be allowed in the
#   repository.  By default they won't be.
# hooks.denycreatebranch
#   This boolean sets whether remotely creating branches will be denied
#   in the repository.  By default this is allowed.
#

# --- Command line
refname="$1"
oldrev="$2"
newrev="$3"

# --- Safety check
if [ -z "$GIT_DIR" ]; then
	echo "Don't run this script from the command line." >&2
	echo " (if you want, you could supply GIT_DIR then run" >&2
	echo "  $0 <ref> <oldrev> <newrev>)" >&2
	exit 1
fi

if [ -z "$refname" -o -z "$oldrev" -o -z "$newrev" ]; then
	echo "usage: $0 <ref> <oldrev> <newrev>" >&2
	exit 1
fi

# --- Config
allowunannotated=$(git config --type=bool hooks.allowunannotated)
allowdeletebranch=$(git config --type=bool hooks.allowdeletebranch)
denycreatebranch=$(git config --type=bool hooks.denycreatebranch)
allowdeletetag=$(git config --type=bool hooks.allowdeletetag)
allowmodifytag=$(git config --type=bool hooks.allowmodifytag)

# check for no description
projectdesc=$(sed -e '1q' "$GIT_DIR/description")
case "$projectdesc" in
"Unnamed repository"* | "")
	echo "*** Project description file hasn't been set" >&2
	exit 1
	;;
esac

# --- Check types
# if $newrev is 0000...0000, it's a commit to delete a ref.
zero=$(git hash-object --stdin </dev/null | tr '[0-9a-f]' '0')
if [ "$newrev" = "$zero" ]; then
	newrev_type=delete
else
	newrev_type=$(git cat-file -t $newrev)
fi

case "$refname","$newrev_type" in
	refs/tags/*,commit)
		# un-annotated tag
		short_refname=${refname##refs/tags/}
		if [ "$allowunannotated" != "true" ]; then
			echo "*** The un-annotated tag, $short_refname, is not allowed in this repository" >&2
			echo "*** Use 'git tag [ -a | -s ]' for tags you want to propagate." >&2
			exit 1
		fi
		;;
	refs/tags/*,delete)
		# delete tag
		if [ "$allowdeletetag" != "true" ]; then
			echo "*** Deleting a tag is not allowed in this repository" >&2
			exit 1
		fi
		;;
	refs/tags/*,tag)
		# annotated tag
		if [ "$allowmodifytag" != "true" ] && git rev-parse $refname > /dev/null 2>&1
		then
			echo "*** Tag '$refname' already exists." >&2
			echo "*** Modifying a tag is not allowed in this repository." >&2
			exit 1
		fi
		;;
	refs/heads/*,commit)
		# branch
		if [ "$oldrev" = "$zero" -a "$denycreatebranch" = "true" ]; then
			echo "*** Creating a branch is not allowed in this repository" >&2
			exit 1
		fi
		;;
	refs/heads/*,delete)
		# delete branch
		if [ "$allowdeletebranch" != "true" ]; then
			echo "*** Deleting a branch is not allowed in this repository" >&2
			exit 1
		fi
		;;
	refs/remotes/*,commit)
		# tracking branch
		;;
	refs/remotes/*,delete)
		# delete tracking branch
		if [ "$allowdeletebranch" != "true" ]; then
			echo "*** Deleting a tracking branch is not allowed in this repository" >&2
			exit 1
		fi
		;;
	*)
		# Anything else (is there anything else?)
		echo "*** Update hook: unknown type of update to ref $refname of type $newrev_type" >&2
		exit 1
		;;
esac

# --- Finished
exit 0

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\info\exclude
```
# git ls-files --others --exclude-from=.git/info/exclude
# Lines that start with '#' are comments.
# For a project mostly in C, the following would be a good set of
# exclude patterns (uncomment them if you want to use them):
# *.[oa]
# *~

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\logs\HEAD
```
0000000000000000000000000000000000000000 6cd69b61f11659d4b01448d2465428b70ef4a211 Rojban <Ruben.Selander@gmail.com> 1700319963 +0100	clone: from https://github.com/Reversehobo/RepoScribe.git
6cd69b61f11659d4b01448d2465428b70ef4a211 776c53e00aace3c2f35dc14c1ccbc09af0147910 Rojban <Ruben.Selander@gmail.com> 1700321244 +0100	commit: Setup.py added
776c53e00aace3c2f35dc14c1ccbc09af0147910 eb370b09b07dc6ad04b0847baee7c61769692a71 Rojban <Ruben.Selander@gmail.com> 1700326064 +0100	commit: core
eb370b09b07dc6ad04b0847baee7c61769692a71 439e0fc82760136ab0f41baf31a94a7aa5199fd8 Rojban <Ruben.Selander@gmail.com> 1700326770 +0100	commit: tests
439e0fc82760136ab0f41baf31a94a7aa5199fd8 7421c9b1415a41ec0195f3236589a29010a03420 Rojban <Ruben.Selander@gmail.com> 1700329345 +0100	commit: cli added
7421c9b1415a41ec0195f3236589a29010a03420 785105e067e9da3a3eccbea4c6019aeb6676020a Rojban <Ruben.Selander@gmail.com> 1700329488 +0100	commit: renamed root_path to path
785105e067e9da3a3eccbea4c6019aeb6676020a 4b1a51cb1f4dc78569018ddd9761894b1ebb235d Rojban <Ruben.Selander@gmail.com> 1700329645 +0100	commit: 0.1.1
4b1a51cb1f4dc78569018ddd9761894b1ebb235d fed4928e262ab7264020ce1c0b0a4eb6a315bb71 Rojban <Ruben.Selander@gmail.com> 1700329893 +0100	commit: missed updating a root path
fed4928e262ab7264020ce1c0b0a4eb6a315bb71 c50f2e3d91ce9e0e64686144bb3fd8d241e94eb8 Rojban <Ruben.Selander@gmail.com> 1700329977 +0100	commit: 0.1.2
c50f2e3d91ce9e0e64686144bb3fd8d241e94eb8 ae010dedb5834c4b20d862efcb41e2fc8dcc13da Rojban <Ruben.Selander@gmail.com> 1700330728 +0100	commit: meeehhh
ae010dedb5834c4b20d862efcb41e2fc8dcc13da e8314728b8aedbd7a2dad8cfae878d6d6313be71 Rojban <Ruben.Selander@gmail.com> 1700330754 +0100	commit: version="0.1.3"
e8314728b8aedbd7a2dad8cfae878d6d6313be71 14caeed37733ecb413bc71ec7fd63355553403d8 Rojban <Ruben.Selander@gmail.com> 1700331966 +0100	commit: ReadMe update
14caeed37733ecb413bc71ec7fd63355553403d8 8e137a1c517b95284fce2c1e4ccbb67b17a814d5 Rojban <Ruben.Selander@gmail.com> 1700333103 +0100	commit: Added Planned Features
8e137a1c517b95284fce2c1e4ccbb67b17a814d5 77fc0b2c8158c8b9e635ff7b01912e79a18a24b5 Rojban <Ruben.Selander@gmail.com> 1700335087 +0100	pull --tags origin main: Fast-forward
77fc0b2c8158c8b9e635ff7b01912e79a18a24b5 c6bba035c8acba3cf5d5608eb225695be5a567b7 Rojban <Ruben.Selander@gmail.com> 1700336326 +0100	pull --tags origin main: Fast-forward
c6bba035c8acba3cf5d5608eb225695be5a567b7 94731b3daab0022ad2b143a236d90724986e104c Rojban <Ruben.Selander@gmail.com> 1700862411 +0100	commit: added more langs
94731b3daab0022ad2b143a236d90724986e104c 71b5c6fcb5741cb58ad321ad6fdf76c5f2b8bbf9 Rojban <Ruben.Selander@gmail.com> 1700862413 +0100	pull --tags origin main: Merge made by the 'ort' strategy.
71b5c6fcb5741cb58ad321ad6fdf76c5f2b8bbf9 4861d3a1a7e9eec2815ba9fcb9d000428a1909c0 Rojban <Ruben.Selander@gmail.com> 1700863584 +0100	commit: auto deploy added
4861d3a1a7e9eec2815ba9fcb9d000428a1909c0 c391f1a646519f97c3f9810e87096df7066739a1 Rojban <Ruben.Selander@gmail.com> 1700864074 +0100	commit: new version

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\logs\refs\heads\main
```
0000000000000000000000000000000000000000 6cd69b61f11659d4b01448d2465428b70ef4a211 Rojban <Ruben.Selander@gmail.com> 1700319963 +0100	clone: from https://github.com/Reversehobo/RepoScribe.git
6cd69b61f11659d4b01448d2465428b70ef4a211 776c53e00aace3c2f35dc14c1ccbc09af0147910 Rojban <Ruben.Selander@gmail.com> 1700321244 +0100	commit: Setup.py added
776c53e00aace3c2f35dc14c1ccbc09af0147910 eb370b09b07dc6ad04b0847baee7c61769692a71 Rojban <Ruben.Selander@gmail.com> 1700326064 +0100	commit: core
eb370b09b07dc6ad04b0847baee7c61769692a71 439e0fc82760136ab0f41baf31a94a7aa5199fd8 Rojban <Ruben.Selander@gmail.com> 1700326770 +0100	commit: tests
439e0fc82760136ab0f41baf31a94a7aa5199fd8 7421c9b1415a41ec0195f3236589a29010a03420 Rojban <Ruben.Selander@gmail.com> 1700329345 +0100	commit: cli added
7421c9b1415a41ec0195f3236589a29010a03420 785105e067e9da3a3eccbea4c6019aeb6676020a Rojban <Ruben.Selander@gmail.com> 1700329488 +0100	commit: renamed root_path to path
785105e067e9da3a3eccbea4c6019aeb6676020a 4b1a51cb1f4dc78569018ddd9761894b1ebb235d Rojban <Ruben.Selander@gmail.com> 1700329645 +0100	commit: 0.1.1
4b1a51cb1f4dc78569018ddd9761894b1ebb235d fed4928e262ab7264020ce1c0b0a4eb6a315bb71 Rojban <Ruben.Selander@gmail.com> 1700329893 +0100	commit: missed updating a root path
fed4928e262ab7264020ce1c0b0a4eb6a315bb71 c50f2e3d91ce9e0e64686144bb3fd8d241e94eb8 Rojban <Ruben.Selander@gmail.com> 1700329977 +0100	commit: 0.1.2
c50f2e3d91ce9e0e64686144bb3fd8d241e94eb8 ae010dedb5834c4b20d862efcb41e2fc8dcc13da Rojban <Ruben.Selander@gmail.com> 1700330728 +0100	commit: meeehhh
ae010dedb5834c4b20d862efcb41e2fc8dcc13da e8314728b8aedbd7a2dad8cfae878d6d6313be71 Rojban <Ruben.Selander@gmail.com> 1700330754 +0100	commit: version="0.1.3"
e8314728b8aedbd7a2dad8cfae878d6d6313be71 14caeed37733ecb413bc71ec7fd63355553403d8 Rojban <Ruben.Selander@gmail.com> 1700331966 +0100	commit: ReadMe update
14caeed37733ecb413bc71ec7fd63355553403d8 8e137a1c517b95284fce2c1e4ccbb67b17a814d5 Rojban <Ruben.Selander@gmail.com> 1700333103 +0100	commit: Added Planned Features
8e137a1c517b95284fce2c1e4ccbb67b17a814d5 77fc0b2c8158c8b9e635ff7b01912e79a18a24b5 Rojban <Ruben.Selander@gmail.com> 1700335087 +0100	pull --tags origin main: Fast-forward
77fc0b2c8158c8b9e635ff7b01912e79a18a24b5 c6bba035c8acba3cf5d5608eb225695be5a567b7 Rojban <Ruben.Selander@gmail.com> 1700336326 +0100	pull --tags origin main: Fast-forward
c6bba035c8acba3cf5d5608eb225695be5a567b7 94731b3daab0022ad2b143a236d90724986e104c Rojban <Ruben.Selander@gmail.com> 1700862411 +0100	commit: added more langs
94731b3daab0022ad2b143a236d90724986e104c 71b5c6fcb5741cb58ad321ad6fdf76c5f2b8bbf9 Rojban <Ruben.Selander@gmail.com> 1700862413 +0100	pull --tags origin main: Merge made by the 'ort' strategy.
71b5c6fcb5741cb58ad321ad6fdf76c5f2b8bbf9 4861d3a1a7e9eec2815ba9fcb9d000428a1909c0 Rojban <Ruben.Selander@gmail.com> 1700863584 +0100	commit: auto deploy added
4861d3a1a7e9eec2815ba9fcb9d000428a1909c0 c391f1a646519f97c3f9810e87096df7066739a1 Rojban <Ruben.Selander@gmail.com> 1700864074 +0100	commit: new version

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\logs\refs\remotes\origin\HEAD
```
0000000000000000000000000000000000000000 6cd69b61f11659d4b01448d2465428b70ef4a211 Rojban <Ruben.Selander@gmail.com> 1700319963 +0100	clone: from https://github.com/Reversehobo/RepoScribe.git

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\logs\refs\remotes\origin\main
```
6cd69b61f11659d4b01448d2465428b70ef4a211 776c53e00aace3c2f35dc14c1ccbc09af0147910 Rojban <Ruben.Selander@gmail.com> 1700321249 +0100	update by push
776c53e00aace3c2f35dc14c1ccbc09af0147910 eb370b09b07dc6ad04b0847baee7c61769692a71 Rojban <Ruben.Selander@gmail.com> 1700326068 +0100	update by push
eb370b09b07dc6ad04b0847baee7c61769692a71 439e0fc82760136ab0f41baf31a94a7aa5199fd8 Rojban <Ruben.Selander@gmail.com> 1700326775 +0100	update by push
439e0fc82760136ab0f41baf31a94a7aa5199fd8 7421c9b1415a41ec0195f3236589a29010a03420 Rojban <Ruben.Selander@gmail.com> 1700329349 +0100	update by push
7421c9b1415a41ec0195f3236589a29010a03420 785105e067e9da3a3eccbea4c6019aeb6676020a Rojban <Ruben.Selander@gmail.com> 1700329493 +0100	update by push
785105e067e9da3a3eccbea4c6019aeb6676020a 4b1a51cb1f4dc78569018ddd9761894b1ebb235d Rojban <Ruben.Selander@gmail.com> 1700329668 +0100	update by push
4b1a51cb1f4dc78569018ddd9761894b1ebb235d fed4928e262ab7264020ce1c0b0a4eb6a315bb71 Rojban <Ruben.Selander@gmail.com> 1700329897 +0100	update by push
fed4928e262ab7264020ce1c0b0a4eb6a315bb71 c50f2e3d91ce9e0e64686144bb3fd8d241e94eb8 Rojban <Ruben.Selander@gmail.com> 1700329982 +0100	update by push
c50f2e3d91ce9e0e64686144bb3fd8d241e94eb8 ae010dedb5834c4b20d862efcb41e2fc8dcc13da Rojban <Ruben.Selander@gmail.com> 1700330732 +0100	update by push
ae010dedb5834c4b20d862efcb41e2fc8dcc13da e8314728b8aedbd7a2dad8cfae878d6d6313be71 Rojban <Ruben.Selander@gmail.com> 1700330758 +0100	update by push
e8314728b8aedbd7a2dad8cfae878d6d6313be71 14caeed37733ecb413bc71ec7fd63355553403d8 Rojban <Ruben.Selander@gmail.com> 1700331970 +0100	update by push
14caeed37733ecb413bc71ec7fd63355553403d8 8e137a1c517b95284fce2c1e4ccbb67b17a814d5 Rojban <Ruben.Selander@gmail.com> 1700333107 +0100	update by push
8e137a1c517b95284fce2c1e4ccbb67b17a814d5 77fc0b2c8158c8b9e635ff7b01912e79a18a24b5 Rojban <Ruben.Selander@gmail.com> 1700335083 +0100	fetch: fast-forward
77fc0b2c8158c8b9e635ff7b01912e79a18a24b5 c6bba035c8acba3cf5d5608eb225695be5a567b7 Rojban <Ruben.Selander@gmail.com> 1700336320 +0100	fetch: fast-forward
c6bba035c8acba3cf5d5608eb225695be5a567b7 d184bba29426f75d69d3b80a353c6d6b89a55c4a Rojban <Ruben.Selander@gmail.com> 1700429172 +0100	fetch: fast-forward
d184bba29426f75d69d3b80a353c6d6b89a55c4a 71b5c6fcb5741cb58ad321ad6fdf76c5f2b8bbf9 Rojban <Ruben.Selander@gmail.com> 1700862415 +0100	update by push
71b5c6fcb5741cb58ad321ad6fdf76c5f2b8bbf9 4861d3a1a7e9eec2815ba9fcb9d000428a1909c0 Rojban <Ruben.Selander@gmail.com> 1700863588 +0100	update by push
4861d3a1a7e9eec2815ba9fcb9d000428a1909c0 c391f1a646519f97c3f9810e87096df7066739a1 Rojban <Ruben.Selander@gmail.com> 1700864077 +0100	update by push

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\02\9263b14e54313018ab1b0a571ec048c6977200
```
Error reading file: 'utf-8' codec can't decode byte 0xd3 in position 6: invalid continuation byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\08\df4d694f0a09f36a3456fe6bb679ef0343f77b
```
Error reading file: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\0a\7e94b8df31e0886faf58147815ef2bc1e895a8
```
Error reading file: 'utf-8' codec can't decode byte 0xce in position 18: invalid continuation byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\0d\3fcae3739feb845db932b11bec6328dc7dad65
```
Error reading file: 'utf-8' codec can't decode byte 0xda in position 6: invalid continuation byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\0d\99d1e622a7d50c1666051d0dbe941dd4cead5f
```
Error reading file: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\0d\a5bb95e56d5bf98dbb107a3613736e05ad5565
```
Error reading file: 'utf-8' codec can't decode byte 0x88 in position 17: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\0d\fd526cce5e596492bb09a71dab7ecd6ec429a9
```
Error reading file: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\0e\97605fd4915d43a7062f6a944672b158d2bf46
```
Error reading file: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\11\adbffa08023c4a51bcc8e2f909e9e5377c7eb0
```
Error reading file: 'utf-8' codec can't decode byte 0xda in position 6: invalid continuation byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\14\81ca38e7ad880ac1e4e143b70935feb78cbb31
```
Error reading file: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\14\caeed37733ecb413bc71ec7fd63355553403d8
```
Error reading file: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\15\a7131001c87bcf3956b9711c104df653187180
```
Error reading file: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\18\ea54a01de0d24dd1f5316cdb8a07e7350191d4
```
Error reading file: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\1b\c71b01fd55740c39e325bf89ce703f2428052f
```
Error reading file: 'utf-8' codec can't decode byte 0xb0 in position 9: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\2b\95544d5cf7528bd75c045daaf6bb565dbae0b6
```
Error reading file: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\2e\c49b6a519c9a6e938bfac52986405131a6d2ed
```
Error reading file: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\31\ee8b6d6b6a094cd136f032646ad79578f3d4b0
```
Error reading file: 'utf-8' codec can't decode byte 0xb0 in position 9: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\37\c0b0e3f9e7c85105fe091ce5c4c4e2a470baee
```
Error reading file: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\39\bfccfc9591e5fcb1cd682b92b66d8af72033d8
```
Error reading file: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\43\9e0fc82760136ab0f41baf31a94a7aa5199fd8
```
Error reading file: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\43\c6a50af0832c07ed331b76151a3523b3d7b3f9
```
Error reading file: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\45\b7266650e42d22d5290df7910ec299902ad207
```
Error reading file: 'utf-8' codec can't decode byte 0xd3 in position 6: invalid continuation byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\48\61d3a1a7e9eec2815ba9fcb9d000428a1909c0
```
Error reading file: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\49\14b2c56c497980fa3053df403a2a339fc519d3
```
Error reading file: 'utf-8' codec can't decode byte 0xda in position 6: invalid continuation byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\4b\1a51cb1f4dc78569018ddd9761894b1ebb235d
```
Error reading file: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\57\13a1197f54a9d2d54f218ed1cd4918c0c2ad0c
```
Error reading file: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\59\112014b720e29ae278772de0cdb10bab533d01
```
Error reading file: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\5a\64c4eebca02c6fc027da18900ac9077d70e9cb
```
Error reading file: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\5d\2009515ae5d7d699a10cfc7688f881fac3a34a
```
Error reading file: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\5d\a68ef8ee775c55124a67bd4de983bc314f6309
```
Error reading file: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\60\91c0c4b14dd9552e2a10f316f6d68490e287e1
```
Error reading file: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\68\bc17f9ff2104a9d7b6777058bb4c343ca72609
```
Error reading file: 'utf-8' codec can't decode byte 0xad in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\6c\9b38ac6722147bb55a1c6e4f4a0ec112ae7ee0
```
Error reading file: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\6d\96ae3fa7d6a1d34dae261fc0bb1ad784c24e9f
```
Error reading file: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\6f\9bcf004156026c7251e518e31b5cc1bfa6be6c
```
Error reading file: 'utf-8' codec can't decode byte 0xc1 in position 4: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\71\b5c6fcb5741cb58ad321ad6fdf76c5f2b8bbf9
```
Error reading file: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\74\21c9b1415a41ec0195f3236589a29010a03420
```
Error reading file: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\74\2348c4bddfb42d0915ff89c893aedd96bc5bc8
```
Error reading file: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\77\6c53e00aace3c2f35dc14c1ccbc09af0147910
```
Error reading file: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\77\fc0b2c8158c8b9e635ff7b01912e79a18a24b5
```
Error reading file: 'utf-8' codec can't decode byte 0x91 in position 3: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\78\5105e067e9da3a3eccbea4c6019aeb6676020a
```
Error reading file: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\79\1e654b6b17d667af8c4175572fcabb056fc28f
```
Error reading file: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\7b\397a8d282fa47ef99ce33b7382084cba9f1422
```
Error reading file: 'utf-8' codec can't decode byte 0x95 in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\89\029b2650f940aa7949b933ec83fbee9cf2db63
```
Error reading file: 'utf-8' codec can't decode byte 0xb0 in position 9: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\8a\034854fea90f30d11a725daa7600e683ea9f8a
```
Error reading file: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\8e\137a1c517b95284fce2c1e4ccbb67b17a814d5
```
Error reading file: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\8e\6d2f56145c81deea29eb1f6804f1a556f5cb2d
```
Error reading file: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\94\731b3daab0022ad2b143a236d90724986e104c
```
Error reading file: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\a0\7bee24098bf714bc3faa72e4924b57ce1cfd1d
```
Error reading file: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\a2\69f541b254527800a8ea3ce1619e7e5ed70529
```
Error reading file: 'utf-8' codec can't decode byte 0xb0 in position 9: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\a5\eee348864e8b1324100a9126e1d9e6af9327c9
```
Error reading file: 'utf-8' codec can't decode byte 0x91 in position 3: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\a7\20ad65b3e8206d8f4764530db8a3bfc7a55383
```
Error reading file: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\ae\010dedb5834c4b20d862efcb41e2fc8dcc13da
```
Error reading file: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\b5\211a382e87d26996acfc21fd85b1fc1429d1c3
```
Error reading file: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\c1\8bf1d8a25222f5edae47c6e1dbed98cc2ec5ef
```
Error reading file: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\c3\91f1a646519f97c3f9810e87096df7066739a1
```
Error reading file: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\c5\0f2e3d91ce9e0e64686144bb3fd8d241e94eb8
```
Error reading file: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\c6\bba035c8acba3cf5d5608eb225695be5a567b7
```
Error reading file: 'utf-8' codec can't decode byte 0x91 in position 3: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\ca\6f79443a08be64d1eab3fde4957099334f3846
```
Error reading file: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\d1\84bba29426f75d69d3b80a353c6d6b89a55c4a
```
Error reading file: 'utf-8' codec can't decode byte 0x91 in position 3: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\d6\06601d38ee0048bbe85977bd69306bce9cb705
```
Error reading file: 'utf-8' codec can't decode byte 0xb0 in position 9: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\d8\21e86d44bb279e3af60b6d8d77dbdf100ce751
```
Error reading file: 'utf-8' codec can't decode byte 0xb4 in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\df\654f47a54cb6024984236c5e1956d482b92c77
```
Error reading file: 'utf-8' codec can't decode byte 0xb0 in position 9: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\e6\9de29bb2d1d6434b8b29ae775ad8c2e48c5391
```
Error reading file: 'utf-8' codec can't decode byte 0xca in position 3: invalid continuation byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\e8\314728b8aedbd7a2dad8cfae878d6d6313be71
```
Error reading file: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\e9\42db00e57cb3b7c9423e5600d968042aa14cde
```
Error reading file: 'utf-8' codec can't decode byte 0xb4 in position 8: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\e9\de4f013e417f6f9965c30cb9d4fda8a54b5785
```
Error reading file: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\eb\370b09b07dc6ad04b0847baee7c61769692a71
```
Error reading file: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\ee\80ef14265880a5519b4aac6a86564ad3d851b7
```
Error reading file: 'utf-8' codec can't decode byte 0xdd in position 4: invalid continuation byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\f7\7a28dcbaa1e535b73b01abdcad5f5c808920ad
```
Error reading file: 'utf-8' codec can't decode byte 0x91 in position 3: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\f9\47fded18b520344bfece7f2064f55cffd254e7
```
Error reading file: 'utf-8' codec can't decode byte 0x85 in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\fe\0ed33d511390c18480563f84ab156c0d24c9d2
```
Error reading file: 'utf-8' codec can't decode byte 0xd0 in position 18: invalid continuation byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\fe\d4928e262ab7264020ce1c0b0a4eb6a315bb71
```
Error reading file: 'utf-8' codec can't decode byte 0x9d in position 2: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\pack\pack-b8ceec86b42ba8a4196c3825e078ece039a635dd.idx
```
Error reading file: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\pack\pack-b8ceec86b42ba8a4196c3825e078ece039a635dd.pack
```
Error reading file: 'utf-8' codec can't decode byte 0x91 in position 12: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\objects\pack\pack-b8ceec86b42ba8a4196c3825e078ece039a635dd.rev
```
Error reading file: 'utf-8' codec can't decode byte 0xb8 in position 28: invalid start byte

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\refs\heads\main
```
c391f1a646519f97c3f9810e87096df7066739a1

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\refs\remotes\origin\HEAD
```
ref: refs/remotes/origin/main

```

## File: C:\Users\Admin\Documents\RepoScribe\.git\refs\remotes\origin\main
```
c391f1a646519f97c3f9810e87096df7066739a1

```

## File: C:\Users\Admin\Documents\RepoScribe\reposcribe\cli.py
```python
import argparse
import os
from .core import create_doc_file


def main():
    parser = argparse.ArgumentParser(description="Generate Markdown documentation for a project directory.")
    parser.add_argument(
        "root_path",
        nargs="?",
        default=os.getcwd(),
        type=str,
        help="Path to the root of the project. Defaults to the current working directory.",
    )
    parser.add_argument(
        "save_path",
        nargs="?",
        default=os.path.join(os.getcwd(), "reposcribe.md"),
        type=str,
        help="Path to save the generated Markdown file. Defaults to 'reposcribe.md' in the current working directory.",
    )
    args = parser.parse_args()

    create_doc_file(root_path=args.root_path, save_path=args.save_path)


if __name__ == "__main__":
    main()

```

## File: C:\Users\Admin\Documents\RepoScribe\reposcribe\core.py
```python
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

```

## File: C:\Users\Admin\Documents\RepoScribe\reposcribe\__init__.py
```python

```

## Directory Structure
```
- .env
- .git/
    - COMMIT_EDITMSG
    - FETCH_HEAD
    - HEAD
    - ORIG_HEAD
    - config
    - description
    - hooks/
        - applypatch-msg.sample
        - commit-msg.sample
        - fsmonitor-watchman.sample
        - post-update.sample
        - pre-applypatch.sample
        - pre-commit.sample
        - pre-merge-commit.sample
        - pre-push.sample
        - pre-rebase.sample
        - pre-receive.sample
        - prepare-commit-msg.sample
        - push-to-checkout.sample
        - sendemail-validate.sample
        - update.sample
    - index
    - info/
        - exclude
    - logs/
        - HEAD
        - refs/
            - heads/
                - main
            - remotes/
                - origin/
                    - HEAD
                    - main
    - objects/
        - 02/
            - 9263b14e54313018ab1b0a571ec048c6977200
        - 08/
            - df4d694f0a09f36a3456fe6bb679ef0343f77b
        - 0a/
            - 7e94b8df31e0886faf58147815ef2bc1e895a8
        - 0d/
            - 3fcae3739feb845db932b11bec6328dc7dad65
            - 99d1e622a7d50c1666051d0dbe941dd4cead5f
            - a5bb95e56d5bf98dbb107a3613736e05ad5565
            - fd526cce5e596492bb09a71dab7ecd6ec429a9
        - 0e/
            - 97605fd4915d43a7062f6a944672b158d2bf46
        - 11/
            - adbffa08023c4a51bcc8e2f909e9e5377c7eb0
        - 14/
            - 81ca38e7ad880ac1e4e143b70935feb78cbb31
            - caeed37733ecb413bc71ec7fd63355553403d8
        - 15/
            - a7131001c87bcf3956b9711c104df653187180
        - 18/
            - ea54a01de0d24dd1f5316cdb8a07e7350191d4
        - 1b/
            - c71b01fd55740c39e325bf89ce703f2428052f
        - 2b/
            - 95544d5cf7528bd75c045daaf6bb565dbae0b6
        - 2e/
            - c49b6a519c9a6e938bfac52986405131a6d2ed
        - 31/
            - ee8b6d6b6a094cd136f032646ad79578f3d4b0
        - 37/
            - c0b0e3f9e7c85105fe091ce5c4c4e2a470baee
        - 39/
            - bfccfc9591e5fcb1cd682b92b66d8af72033d8
        - 43/
            - 9e0fc82760136ab0f41baf31a94a7aa5199fd8
            - c6a50af0832c07ed331b76151a3523b3d7b3f9
        - 45/
            - b7266650e42d22d5290df7910ec299902ad207
        - 48/
            - 61d3a1a7e9eec2815ba9fcb9d000428a1909c0
        - 49/
            - 14b2c56c497980fa3053df403a2a339fc519d3
        - 4b/
            - 1a51cb1f4dc78569018ddd9761894b1ebb235d
        - 57/
            - 13a1197f54a9d2d54f218ed1cd4918c0c2ad0c
        - 59/
            - 112014b720e29ae278772de0cdb10bab533d01
        - 5a/
            - 64c4eebca02c6fc027da18900ac9077d70e9cb
        - 5d/
            - 2009515ae5d7d699a10cfc7688f881fac3a34a
            - a68ef8ee775c55124a67bd4de983bc314f6309
        - 60/
            - 91c0c4b14dd9552e2a10f316f6d68490e287e1
        - 68/
            - bc17f9ff2104a9d7b6777058bb4c343ca72609
        - 6c/
            - 9b38ac6722147bb55a1c6e4f4a0ec112ae7ee0
        - 6d/
            - 96ae3fa7d6a1d34dae261fc0bb1ad784c24e9f
        - 6f/
            - 9bcf004156026c7251e518e31b5cc1bfa6be6c
        - 71/
            - b5c6fcb5741cb58ad321ad6fdf76c5f2b8bbf9
        - 74/
            - 21c9b1415a41ec0195f3236589a29010a03420
            - 2348c4bddfb42d0915ff89c893aedd96bc5bc8
        - 77/
            - 6c53e00aace3c2f35dc14c1ccbc09af0147910
            - fc0b2c8158c8b9e635ff7b01912e79a18a24b5
        - 78/
            - 5105e067e9da3a3eccbea4c6019aeb6676020a
        - 79/
            - 1e654b6b17d667af8c4175572fcabb056fc28f
        - 7b/
            - 397a8d282fa47ef99ce33b7382084cba9f1422
        - 89/
            - 029b2650f940aa7949b933ec83fbee9cf2db63
        - 8a/
            - 034854fea90f30d11a725daa7600e683ea9f8a
        - 8e/
            - 137a1c517b95284fce2c1e4ccbb67b17a814d5
            - 6d2f56145c81deea29eb1f6804f1a556f5cb2d
        - 94/
            - 731b3daab0022ad2b143a236d90724986e104c
        - a0/
            - 7bee24098bf714bc3faa72e4924b57ce1cfd1d
        - a2/
            - 69f541b254527800a8ea3ce1619e7e5ed70529
        - a5/
            - eee348864e8b1324100a9126e1d9e6af9327c9
        - a7/
            - 20ad65b3e8206d8f4764530db8a3bfc7a55383
        - ae/
            - 010dedb5834c4b20d862efcb41e2fc8dcc13da
        - b5/
            - 211a382e87d26996acfc21fd85b1fc1429d1c3
        - c1/
            - 8bf1d8a25222f5edae47c6e1dbed98cc2ec5ef
        - c3/
            - 91f1a646519f97c3f9810e87096df7066739a1
        - c5/
            - 0f2e3d91ce9e0e64686144bb3fd8d241e94eb8
        - c6/
            - bba035c8acba3cf5d5608eb225695be5a567b7
        - ca/
            - 6f79443a08be64d1eab3fde4957099334f3846
        - d1/
            - 84bba29426f75d69d3b80a353c6d6b89a55c4a
        - d6/
            - 06601d38ee0048bbe85977bd69306bce9cb705
        - d8/
            - 21e86d44bb279e3af60b6d8d77dbdf100ce751
        - df/
            - 654f47a54cb6024984236c5e1956d482b92c77
        - e6/
            - 9de29bb2d1d6434b8b29ae775ad8c2e48c5391
        - e8/
            - 314728b8aedbd7a2dad8cfae878d6d6313be71
        - e9/
            - 42db00e57cb3b7c9423e5600d968042aa14cde
            - de4f013e417f6f9965c30cb9d4fda8a54b5785
        - eb/
            - 370b09b07dc6ad04b0847baee7c61769692a71
        - ee/
            - 80ef14265880a5519b4aac6a86564ad3d851b7
        - f7/
            - 7a28dcbaa1e535b73b01abdcad5f5c808920ad
        - f9/
            - 47fded18b520344bfece7f2064f55cffd254e7
        - fe/
            - 0ed33d511390c18480563f84ab156c0d24c9d2
            - d4928e262ab7264020ce1c0b0a4eb6a315bb71
        - info/
        - pack/
            - pack-b8ceec86b42ba8a4196c3825e078ece039a635dd.idx
            - pack-b8ceec86b42ba8a4196c3825e078ece039a635dd.pack
            - pack-b8ceec86b42ba8a4196c3825e078ece039a635dd.rev
    - packed-refs
    - refs/
        - heads/
            - main
        - remotes/
            - origin/
                - HEAD
                - main
        - tags/
- .gitignore
- LICENSE
- README.md
- deploy.py
- reposcribe/
    - __init__.py
    - cli.py
    - core.py
- reposcribe_logo.png
- setup.py
- tests/
```