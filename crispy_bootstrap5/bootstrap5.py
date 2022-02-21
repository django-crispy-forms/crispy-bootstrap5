from crispy_forms.bootstrap import Accordion  # type: ignore
from crispy_forms.layout import Field  # type: ignore


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

    def __init__(
        self,
        *args,
        flush: bool = False,
        always_open: bool = False,
        css_id: str = None,
        css_class: str = None,
        template: str = None,
        **kwargs,
    ) -> None:
        super().__init__(
            *args,
            css_id=css_id,
            css_class=css_class,
            template=template or self.template,
            **kwargs,
        )
        self.flush = flush
        self.always_open = always_open

        if self.always_open:
            for accordion_group in self.fields:
                accordion_group.always_open = True
