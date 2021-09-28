import os

from setuptools import setup

VERSION = "0.6"


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
    url="https://github.com/django-crispy-forms/crispy-bootstrap5",
    project_urls={
        "Issues": "https://github.com/django-crispy-forms/crispy-bootstrap5/issues",
        "CI": "https://github.com/django-crispy-forms/crispy-bootstrap5/actions",
        "Changelog": (
            "https://github.com/django-crispy-forms/crispy-bootstrap5/releases"
        ),
    },
    license="MIT",
    version=VERSION,
    packages=["crispy_bootstrap5"],
    install_requires=["django-crispy-forms>=1.13.0", "django>=2.2"],
    extras_require={"test": ["pytest", "pytest-django"]},
    tests_require=["crispy-bootstrap5[test]"],
    python_requires=">=3.6",
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
