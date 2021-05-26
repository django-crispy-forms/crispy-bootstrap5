# crispy-bootstrap5

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/smithdc1/crispy-bootstrap5/blob/main/LICENSE)

Bootstrap5 template pack for django-crispy-forms

## Installation

Install this plugin using `pip`:

    $ pip install crispy-bootstrap5

## Usage

You will need to update your project's settings file to add ``crispy_forms``
and ``crispy_bootstrap5`` to your projects ``INSTALLED_APPS``. Also set
``bootstrap5`` as and allowed template pack and as the default template pack
for your project::

    INSTALLED_APPS = (
        ...
        "crispy_forms",
        "crispy_bootstrap5",
        ...
    )

    CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

    CRISPY_TEMPLATE_PACK = "bootstrap5"

## What's new?

Bootstrap 5 introduces [floating labels](https://getbootstrap.com/docs/5.0/forms/floating-labels/).
This template pack include a layout object to use this input type::

    from crispy_bootstrap5.bootstrap5 import FloatingField
    
    # then in your Layout
    ... Layout(
        FloatingField("first_name"),
    )

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:

    cd crispy-bootstrap5
    python -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
