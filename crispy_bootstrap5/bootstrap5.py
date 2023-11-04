from crispy_forms.bootstrap import Accordion
from crispy_forms.layout import Field


class FloatingField(Field):
    template = "bootstrap5/layout/floating_field.html"


class BS5Accordion(Accordion):
    """
    Bootstrap5 Accordion menu object. It wraps `AccordionGroup` objects in a
    container. It also allows the usage of accordion-flush, introduced in bootstrap5::

        BS5Accordion(
            AccordionGroup("group name", "form_field_1", "form_field_2"),
            AccordionGroup("another group name", "form_field"),
            flush=True,
            always_open=True
        )
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flush = kwargs.pop("flush", False)
        self.always_open = kwargs.pop("always_open", False)

        if self.always_open:
            for accordion_group in self.fields:
                accordion_group.always_open = True


class Switch(Field):
    template = "bootstrap5/layout/switch.html"
