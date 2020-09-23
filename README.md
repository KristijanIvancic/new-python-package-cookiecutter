# Cookiecutter template for Python packages

This repository is used as a template for the [Cookiecutter tool](https://cookiecutter.readthedocs.io/en/1.7.0/index.html). You can install Cookiecutter with `pip`:

```sh
pip install cookiecutter
```

If you want to use conda, you'll have to add [`conda-forge`](https://conda-forge.org/) to your channels first:

```shell
conda config --add channels conda-forge
conda install cookiecutter
```

## Usage

Create a [new repo](https://help.github.com/en/github/getting-started-with-github/create-a-repo) but **don't** initialize it with a `README.md` or `.gitignore`. Just a completely empty repo. Let's say it's called `NewCompany-PythonLibrary`. On your computer, position yourself inside the folder where you usually store git projects (let's call it `git/`), and activate the virtual environment:

```sh
$ cd git/
$ source activate cookiecutter
```

Next, call the cookiecutter command and give it the link to this repository. Not the new one you just created, _this one_, that holds the file you are just reading:

```shell
$ cookiecutter https://github.com/company/cookiecutter-python-library/
```

Cookiecutter will use it as a template to create all the files you need to start building your Python library. It will ask you some questions to help set up the repo:

```sh
repo_name [NewCompany-PythonLibrary]:
package_name [company_package]:
initial_version_number [0.0.1]:
short_description [A new in-house Python library.]:
maintainer [team_name]:
maintainer_email [tech@company.com]:
```

If you want to take the default value in [brackets], just hit return. But the first one, `repo_name`, should be the same as the new GitHub repo you just created, `NewCompany-PythonLibrary`. `package_name` is the name you will `import` in Python, so call it something meaningful.

You should now have a folder `NewCompany-PythonLibrary` with a bunch of files inside. Enter the folder, initialize git, connect it with GitHub, and upload the files Cookiecutter created:

```sh
# Enter the repo
$ cd `NewCompany-PythonLibrary`
# Initialize git
$ git init
# Add all files
$ git add .
# Create a commit
$ git commit -m "First commit"
# Set the new remote
$ git remote add origin [remote repository URL, the one pointing to `NewCompany-PythonLibrary`]
# Verify the new remote URL
$ git remote -v
# Push the changes to remote while creating the master branch
$ git push -u origin master
```

Your repository is now set up with the template and you can begin coding.

## Configuration

Cookiecutter uses the [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) templating language. Everything you see with double curly braces will be replaced by a configuration option you write when creating the project, or with the default defined in `cookiecutter.json`

If you want to add, remove or change any of the options, edit `cookiecutter.json`

### Example `cookiecutter.json`

```json
{
  "repo_name": "NewCompany-PythonLibrary",
  "package_name": "company_package",
  "initial_version_number": "0.0.1",
  "short_description": "A new in-house Python library.",
  "maintainer": "team_name",
  "maintainer_email": "tech@company.com"
}
```
