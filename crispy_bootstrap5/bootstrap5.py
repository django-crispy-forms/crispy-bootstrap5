from crispy_forms.layout import Field


class FloatingField(Field):
    template = "bootstrap5/layout/floating_field.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs["placeholder"] = self.fields[0]
