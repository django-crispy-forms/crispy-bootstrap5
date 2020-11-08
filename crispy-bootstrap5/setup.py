from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="crispy-bootstrap5",
    description="Bootstrap5 template pack for django-crispy-forms",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="David Smith",
    url="https://github.com/smithdc1/crispy-bootstrap5",
    project_urls={
        "Issues": "https://github.com/smithdc1/crispy-bootstrap5/issues",
        "CI": "https://github.com/smithdc1/crispy-bootstrap5/actions",
        "Changelog": "https://github.com/smithdc1/crispy-bootstrap5/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["crispy_bootstrap5"],
    install_requires=["django-crispy-forms>=1.9.2", "django>=2.2"],
    extras_require={"test": ["pytest", "pytest-django"]},
    tests_require=["crispy-bootstrap5[test]"],
    python_requires=">=3.6",
)
