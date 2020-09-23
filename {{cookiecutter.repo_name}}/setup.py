from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="{{ cookiecutter.package_name }}",
    version="{{ cookiecutter.initial_version_number }}",
    description="{{ cookiecutter.short_description }}",
    maintainer="{{ cookiecutter.maintainer}}",
    maintaner_email="{{ cookiecutter.maintainer_email }}",
    packages=find_packages("src"),
    package_dir={"": "src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=5.3.0",
            "pytest-cov>=2.8.1",
            "pytest-env>=0.6.2",
            "black>=19.10b0",
            "tox>=3.15.1",
            "pre-commit>=2.4.0",
            "isort>=4.3.21",
            "flake8<3.8",
            "mypy>=0.770",
            "pdoc3>=0.8.1",
            "bump2version>=1.0.0",
        ]
    },
)
