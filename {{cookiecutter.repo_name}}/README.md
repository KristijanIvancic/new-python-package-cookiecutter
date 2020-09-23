# {{ cookiecutter.repo_name }}

{{ cookiecutter.short_description }}

## Current version: {{ cookiecutter.initial_version_number }}

## Installation

### Local

To get the latest version of this library, create and activate a virtual environment, then run:

```sh
$ pip install git+ssh://git@https://github.com/company/{{ cookiecutter.repo_name }}.git
```

If you want to install it from `requirement.txt`:

```sh
# requirements.txt
git+ssh://git@github.com/company/{{ cookiecutter.repo_name }}@{version_number}#egg={{ cookiecutter.package_name }}
```

Make sure to replace `{version_number}` with an actual version.

Once the library is installed, you can import it like any other Python library. For example:

```python
import {{ cookiecutter.package_name }}
```

### Production

Write instructions for installing in your production environment here. This cookiecutter has a `ci/` folder with a `buildspec.yml` file necessary for AWS CodeBuild.

## Developing this library

To contribute to this library, you need to install it with the tools necessary to run tests and hooks. Create and activate a virtual environment, clone the repo, and install it:

```sh
$ git clone https://github.com/company/{{ cookiecutter.repo_name }}.git
$ cd {{ cookiecutter.repo_name }}
$ pip install -e .[dev]
```

The `-e` switch installs the library in [development mode](https://setuptools.readthedocs.io/en/latest/setuptools.html?highlight=development%20mode#development-mode), and it needs to know where `setup.py` is. Since it's in the repo you are currently in, the next argument is `.` to tell `pip` to use `setup.py` from the _current folder_.

And finally, `[dev]` tells `pip` that the `dev` dependencies should be installed. `[dev]` dependencies are packages that you will need for running tests, linting, etc. They are specified inside `setup.py`, under `extras_require`.

The next step is installing pre-commit hooks. This will ensure that linters and other checks run every time you type `git commit` and tests run every time you tipe `git push`. The commit and push commands will not go through if the checks fail. Run the following two commands:

```sh
# Installs pre-commit hooks
$ pre-commit install
# Installs pre-push hooks
$ pre-commit install --hook-type pre-push
```

We are trying to maintain a high standard of quality, so there are a few things to learn before working on this project:

1. [Documentation](#documentation)
2. [Pre-commit Hooks](#pre-commit-hooks)
3. [Testing](#testing)
4. [Static Type Checking](#static-type-checking)
5. [Dependency Management](#dependency-management)
6. [Releasing and Versioning](#releasing-and-versioning)

### Documentation

The documentation files for this library can be generated from docstrings using the [pdoc](https://github.com/pdoc3/pdoc) tool:

```sh
$ pdoc --output-dir docs/ --html --force -c show_source_code=False src/{{ cookiecutter.package_name }}
```

If the `--html` switch is omitted, the documentation will be generated in Markdown. Whenever a new version of the library is released, the docs should be regenerated. The `--force` switch overwrites the current documentation files. `show_source_code=False` prevents the code itself from being rendered in the documentation.

Both HTML and Markdown documentation files can be found in the `docs/` folder.

### Pre-commit hooks

Keeping track of all the linting, formatting, and analysis tools can be annoying and it's easy to forget something. During peer-review, we don't want to focus on linting. We want to focus on architecture, code design and performance. So we automated the boring stuff with pre-commit hooks.

We used a tool creatively named [pre-commit](https://pre-commit.com/) that creates and installs Git hooks for us. To define the hooks, we need to write a configuration file, call it `.pre-commit-config.yaml` and put it in the root directory. To install the hooks, we need to run the terminal command:

```sh
$ pre-commit install
```

This will take all the hooks from the YAML file and install them in the `.git/hooks/pre-commit` folder, so they will run automatically when you type `git commit` but _before_ the repo is committed. If any of the hooks fail, the commit will not go through.

You can set hooks to run in other stages (e.g. before `git-push`) in the configuration the YAML.

The first line of the YAML is the `repo` property:

```yaml
repo: local
```

It can refer to anything that `git clone` understands, but to use the local YAML file, keep it pointed to `local`.

Next is a list of hooks, for example:

```yaml
hooks:
  - id: isort
    name: isort
    stages: [commit]
    language: system
    entry: isort
    types: [python]
```

Look up the meaning of each property in the [official docs](https://pre-commit.com/#creating-new-hooks).

You can change the stage to something else, like `push` to run the hook when `git push` is executed, but you have to install it separately with:

```sh
$ pre-commit install --hook-type pre-push
```

This is necessary because these hooks go into a different file in the `.git` folder, `.git/hooks/pre-push`.

You can run the hooks before you execute a `git commit` with the `run` command:

```sh
$ pre-commit run --all-files
```

The `--all-files` or `-a` switch is there because `pre-commit` will default to running only on staged files.

You can do a dry run before a `git push` or any other stage:

```sh
$ pre-commit run --hook-stage push --all-files
```

Here's a list of all the hooks we use in this repo:

1. [isort](https://github.com/timothycrosley/isort) - Automatically sorts import statements
2. [black](https://black.readthedocs.io/en/stable/) - An opinionated formatter
3. [flake8](https://flake8.pycqa.org/en/latest/) - Linting
4. [mypy](https://mypy.readthedocs.io/en/stable/) - Static type checking (covered in separate section)
5. [tox](https://tox.readthedocs.io/en/latest/) - Runs tests in multiple environments (covered in separate section)

### Testing

To run all tests with coverage, position yourself in the repository root directory and run the following command:

```sh
$ tox
```

Tox is a tool that can run tests for multiple Python versions, e.g. 3.7, 3.8, etc. It creates a virutal environment for each version and uses it to run the tests. Additionally, if there's a `setup.py` in the repo, it installs it as a library and uses it to run the tests. That is very important because we want to run tests against the installed library as opposed to the code in the repo, because that's what the users will be running.

The configuration for the tests goes into `tox.ini`. Here's an example:

```ini
[tox]
envlist = py37, py38

[testenv]
deps=
  pytest>=5.4.2
  pytest-cov>=2.9.0
  pytest-env>=0.6.2
commands=
  pytest -v --cov test/

[pytest]
minversion= 5.3

[flake8]
max-line-length = 100
```

There are 4 headers:

- The `[tox]` header collects all the configuration for tox itself, in this case choosing two Python versions to test: Python 3.7 and Python 3.8.
- The `[testenv]` header collects the configuration for the virtual environments that will be used to run the tests. In this case, there's a list of libraries that the tests depend on and the command used to run the tests.
- The `[pytest]` header collects `pytest` configuration, which is convenient, because then we don't need to put it in `pytest.ini`.
- Finally, other tools can be configured here, like `[flake8]`. If a tool can read it's configuration from `tox.ini`, prefer to put it here.

It's easy to forget to run tests before opening PRs, so it's useful to have hooks that run them. Running them automatically before every commit, even when it's not a code change, can be overkill. You can set it up as a pre-push hook by putting the following under `hooks` in the `.pre-commit-config.yaml`:

```yaml
- id: tox
      name: tox
      stages: [push]
      language: system
      entry: tox
      types: [python]
      pass_filenames: false
```

### Static Type Checking

Python is a dynamically typed language. This means that the types of variables are inferred during runtime. This makes it very flexible when writing code, but can lead to unexpected runtime errors. But, Python supports type annotations, so you can hint at what the type of each atribute, parameter and return value should be. Then you can use a 3rd party type checker like `mypy` to run static type analysis.

Since static type checking catches problems early and enables us to be more deliberate about our code, we will use it in this library.

Here's an example of type hints:

```python

name: str = "Kristijan"

def multiply(a: int, b:int) -> int:
    "Docstring omitted"
    return a * b
```

Each variable parameter has a type hint and the type of the functino return comes after `->`. Using primitives like `int` and `str` for type hints is fine, but for sequences and mappings it's not so simple. For example:

```python
names: list = ["Charlie", "Kristijan", "Sam"]
coordinates: dict = {"lat": 22.15, "lng": -15.66}
```

This only tells us that `names` is a list, but not the types of the elements inside the list. Same for dictionaries. In this case, we should use the special types from the `typing` module:

```python
from typing import Dict, List

names: List[str] = ["Charlie", "Kristijan", "Sam"]
coordinates: Dict[str, int] = {"lat": 22.15, "lng": -15.66}
```

Now we now `names` is a list of strings and `coordinates` is a dictionary with strings for keys and integers for values.

We will use `mypy` for type checking, which will run as a precommit hook and tell us when we forget to add type hints. It also checks the types of 3rd party libraries which we use, and they might not have type hints, which will throw errors.

There are several ways to mitigate this, but for now we can just ignore checking those libraries. Just add the library to ignore into the `mypy` config file, `mypy.ini` or `setup.cfg`. For example, if we want to ignore type hints for `psycopg2`, add the following to the config file:

```ini
[mypy-psycopg2]
ignore_missing_imports = True
```

Here's a great article on [Python Type Checking](https://realpython.com/python-type-checking/), if you want to learn more.

### Dependency Management

Python libraries do not use `requirements.txt` or similar files. The dependencies are listed inside `setup.py`. You will find all the setup configuration there, inside the call for the `setup()` function.

When you want to add a 3rd party package as a dependancy to this library, list it under `install_requires`. Note that the specific version should be more permissive as opposed to `requirements.txt`. With the requirements file, we want to lock down a specific version, because we know that one works, and we want to always use it.

With libraries, we want to be open to including future bug fixes and upgrades. So instead of locking down the version, make it open-ended. For example, instead of `pandas==1.04` say `pandas>=1.04`.

The dependencies listend under `install_requires` are those that the end user will need to run the library. It shouldn't include packages used when developing the library, like stuff for testing, linting, type checking, etc.

Libraries used for development should go under `extras_require`. This is a dictionary for choosing different sets of dependencies to install. Development dependencies are traditionally grouped under the `dev` key.

So if you download this repo, and want to install `{{ cookiecutter.package_name }}` locally, you would run:

```sh
pip install -e .
```

where `.` just means "the package whose `setup.py` is in this folder". If you want the `def` dependencies, then you would run:

```sh
pip install -e .[dev]
```

Keep in mind that automated tests using `tox` have their own dependency tries listed in `tox.ini`.

### Releasing and Versioning

This library follows [Semantic Versioning](https://semver.org/).

Summary:

Given a version number MAJOR.MINOR.PATCH, increment the:

1. MAJOR version when you make incompatible API changes,
2. MINOR version when you add functionality in a backwards compatible manner, and
3. PATCH version when you make backwards compatible bug fixes.

There are four files where the version number is documented: `setup.py`, `setup.cfg`, `README.md`, and `src/{{ cookiecutter.package_name }}/__init__.py`. You can change all of them at once using a tool called [bumpversion](https://github.com/c4urself/bump2version).

When you're in the environment with the [dev] dependencies for this library installed, type this command into your terminal:

```sh
$ bumpversion [part]
```

Where [part] is the part of the version number to increment: `major`, `minor`, or `patch`. You can do a dry run with:

```sh
$ bumpversion [part] --dry-run --verbose
```

The files that `bumpversion` will change are described in the configuration file `setup.cfg`.

To release a new version of this library, go to it's GitHub repo and click on the _Releases_ tab. Select _Create New Release_ and do the following:

1. Tag the release with a version number.
2. Pick the commit/branch you want to release.
3. Give the release a meaningful title.
4. Describe what's changed.
5. Click _Publish release_
