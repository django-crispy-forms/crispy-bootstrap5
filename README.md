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

Accordions also have new features, such as [Accordion flush](https://getbootstrap.com/docs/5.0/components/accordion/#flush) and [Always open](https://getbootstrap.com/docs/5.0/components/accordion/#always-open).
There is a new layout object to use them::

    from crispy_bootstrap5.bootstrap5 import BS5Accordion

    # then in your Layout
    # if not informed, flush and always_open default to False
    ... Layout(
        BS5Accordion(
            AccordionGroup("group name", "form_field_1", "form_field_2"),
            AccordionGroup("another group name", "form_field"),
            flush=True,
            always_open=True
        )
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
