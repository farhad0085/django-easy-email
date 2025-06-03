import pathlib
from setuptools import setup

# The directory containing this file
BASE_PATH = pathlib.Path(__file__).resolve().parent

# The text of the README file
README = (BASE_PATH / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="django-easy-email",
    version="1.0.0",
    description="A Django extension designed to streamline email management with powerful templates, scheduling, storage, and more.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/farhad0085/django-easy-email",
    author="Farhad Hossain",
    author_email="farhadhossain0085@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=[
        "easy_email",
        "easy_email/migrations",
        "easy_email/loaders",
        "easy_email/backends",
        "easy_email/processors",
    ],
    include_package_data=True,
    install_requires=[
        "django>=3.2",
        "filetype>=1.2.0",
    ],
)

# build
# python setup.py sdist bdist_wheel
# upload to pypi
# twine upload dist/*