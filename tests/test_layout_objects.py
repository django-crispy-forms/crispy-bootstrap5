import random

import django
import pytest
from crispy_forms.bootstrap import (
    Accordion,
    AccordionGroup,
    Alert,
    AppendedText,
    FieldWithButtons,
    InlineCheckboxes,
    InlineField,
    InlineRadios,
    Modal,
    PrependedAppendedText,
    PrependedText,
    StrictButton,
    Tab,
    TabHolder,
)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Layout, MultiWidgetField
from crispy_forms.utils import render_crispy_form
from django import forms
from django.template import Context, Template
from django.test import override_settings
from django.utils.translation import activate, deactivate
from django.utils.translation import gettext as _

from crispy_bootstrap5.bootstrap5 import BS5Accordion, FloatingField, Switch

from .forms import (
    CheckboxesSampleForm,
    CustomCheckboxSelectMultiple,
    CustomRadioSelect,
    GroupedChoiceForm,
    InputsForm,
    SampleForm,
    SampleFormCustomWidgets,
)
from .utils import parse_expected, parse_form

CONVERTERS = {
    "textinput": "inputtext textinput textInput",
    "fileinput": "fileinput fileUpload",
    "passwordinput": "textinput textInput",
}


def test_field_with_custom_template():
    test_form = SampleForm()
    test_form.helper = FormHelper()
    test_form.helper.layout = Layout(
        Field("email", template="custom_field_template.html")
    )

    html = render_crispy_form(test_form)
    assert "<h1>Special custom field</h1>" in html


def test_multiwidget_field():
    template = Template(
        """
        {% load crispy_forms_tags %}
        {% crispy form %}
    """
    )

    test_form = SampleForm()
    test_form.helper = FormHelper()
    test_form.helper.layout = Layout(
        MultiWidgetField(
            "datetime_field",
            attrs=(
                {"rel": "test_dateinput"},
                {"rel": "test_timeinput", "style": "width: 30px;", "type": "hidden"},
            ),
        )
    )

    c = Context({"form": test_form})

    html = template.render(c)

    assert html.count('class="dateinput') == 1
    assert html.count('rel="test_dateinput"') == 1
    assert html.count('rel="test_timeinput"') == 2
    assert html.count('style="width: 30px;"') == 2
    assert html.count('type="hidden"') == 2


def test_field_type_hidden():
    template = Template(
        """
        {% load crispy_forms_tags %}
        {% crispy test_form %}
    """
    )

    test_form = SampleForm()
    test_form.helper = FormHelper()
    test_form.helper.layout = Layout(
        Field("email", type="hidden", data_test=12),
        Field("datetime_field"),
    )

    c = Context({"test_form": test_form})
    html = template.render(c)

    # Check form parameters
    assert html.count('data-test="12"') == 1
    assert html.count('name="email"') == 1
    assert html.count('class="dateinput') == 1
    assert html.count('class="timeinput') == 1


def test_field_wrapper_class(settings):
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.layout = Layout(Field("email", wrapper_class="testing"))

    html = render_crispy_form(form)
    if settings.CRISPY_TEMPLATE_PACK == "bootstrap":
        assert html.count('class="control-group testing"') == 1
    elif settings.CRISPY_TEMPLATE_PACK in ("bootstrap3", "bootstrap4"):
        assert html.count('class="form-group testing"') == 1


def test_html_with_carriage_returns(settings):
    test_form = SampleForm()
    test_form.helper = FormHelper()
    test_form.helper.layout = Layout(
        HTML(
            """
            if (a==b){
                // some comment
                a+1;
                foo();
            }
        """
        )
    )
    html = render_crispy_form(test_form)

    if settings.CRISPY_TEMPLATE_PACK == "uni_form":
        assert html.count("\n") == 23
    elif settings.CRISPY_TEMPLATE_PACK == "bootstrap":
        assert html.count("\n") == 25
    else:
        assert html.count("\n") == 27


def test_i18n():
    activate("es")
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.layout = Layout(HTML(_("Enter a valid value.")))
    html = render_crispy_form(form)
    assert "Introduzca un valor válido" in html

    deactivate()


def test_remove_labels():
    form = SampleForm()
    # remove boolean field as label is still printed in boostrap
    del form.fields["is_company"]

    for fields in form:
        fields.label = False

    html = render_crispy_form(form)

    assert "<label" not in html


@pytest.mark.parametrize(
    "input,expected",
    [
        ("text_input", "text_input.html"),
        ("text_area", "text_area.html"),
        ("checkboxes", "checkboxes.html"),
        ("radio", "radio.html"),
        ("single_checkbox", "single_checkbox.html"),
    ],
)
def test_inputs(input, expected):
    form = InputsForm()
    form.helper = FormHelper()
    form.helper.layout = Layout(input)
    assert parse_form(form) == parse_expected(expected)


class TestBootstrapLayoutObjects:
    def test_custom_django_widget(self):
        # Make sure an inherited RadioSelect gets rendered as it
        form = SampleFormCustomWidgets()
        assert isinstance(form.fields["inline_radios"].widget, CustomRadioSelect)
        form.helper = FormHelper()
        form.helper.layout = Layout("inline_radios")

        html = render_crispy_form(form)
        print(html)
        assert 'class="form-check-input"' in html

        # Make sure an inherited CheckboxSelectMultiple gets rendered as it
        assert isinstance(
            form.fields["checkboxes"].widget, CustomCheckboxSelectMultiple
        )
        form.helper.layout = Layout("checkboxes")
        html = render_crispy_form(form)
        assert 'class="form-check-input"' in html

    @override_settings(CRISPY_CLASS_CONVERTERS=CONVERTERS)
    def test_prepended_appended_text(self):
        test_form = SampleForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(
            PrependedAppendedText(
                "email", "@<>&", "gmail.com", css_class="form-control-lg"
            ),
            AppendedText("password1", "#"),
            PrependedText("password2", "$"),
        )
        if django.VERSION < (5, 0):
            expected = "test_prepended_appended_text_lt50.html"
        else:
            expected = "test_prepended_appended_text.html"
        assert parse_form(test_form) == parse_expected(expected)

    def test_inline_radios(self):
        form = CheckboxesSampleForm()
        form.helper = FormHelper()
        form.helper.layout = Layout(InlineRadios("inline_radios"))
        assert parse_form(form) == parse_expected("inline_radios.html")

    def test_inline_checkboxes(self):
        form = CheckboxesSampleForm()
        form.helper = FormHelper()
        form.helper.layout = InlineRadios("checkboxes")
        assert parse_form(form) == parse_expected("inline_checkboxes.html")

    def test_inline_radios_failing(self):
        form = CheckboxesSampleForm({})
        form.helper = FormHelper()
        form.helper.layout = Layout(InlineRadios("inline_radios"))
        if django.VERSION < (5, 0):
            expected = "inline_radios_failing_lt50.html"
        else:
            expected = "inline_radios_failing.html"
        assert parse_form(form) == parse_expected(expected)

    def test_inline_checkboxes_failing(self):
        form = CheckboxesSampleForm({})
        form.helper = FormHelper()
        form.helper.layout = InlineRadios("checkboxes")
        if django.VERSION < (5, 0):
            expected = "inline_checkboxes_failing_lt50.html"
        else:
            expected = "inline_checkboxes_failing.html"
        assert parse_form(form) == parse_expected(expected)

    @override_settings(CRISPY_CLASS_CONVERTERS=CONVERTERS)
    def test_accordion_and_accordiongroup(self):
        random.seed(0)
        form = SampleForm()
        form.helper = FormHelper()
        form.helper.form_tag = False
        form.helper.layout = Layout(
            Accordion(
                AccordionGroup("one", "first_name"),
                AccordionGroup("two", "password1", "password2"),
            )
        )
        assert parse_form(form) == parse_expected("accordion.html")

    def test_accordion_css_class_is_applied(self):
        classes = 'one two three'
        test_form = SampleForm()
        test_form.helper = FormHelper()
        test_form.helper.form_tag = False
        test_form.helper.layout = Layout(
            Accordion(
                AccordionGroup("one", "first_name"),
                css_class=classes,
                css_id='super-accordion'
            )
        )
        html = render_crispy_form(test_form)

        assert (
                html.count('<div class="accordion %s" id="super-accordion"' % classes)
                == 1
        )

    def test_accordion_active_false_not_rendered(self):
        test_form = SampleForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(
            Accordion(
                AccordionGroup("one", "first_name"),
                # there is no ``active`` kwarg here.
            )
        )

        # The first time, there should be one of them there.
        html = render_crispy_form(test_form)

        accordion_class = "collapse show"

        assert (
            html.count('<div id="one" class="accordion-collapse %s"' % accordion_class)
            == 1
        )

        test_form.helper.layout = Layout(
            Accordion(
                AccordionGroup("one", "first_name", active=False),
            )  # now ``active`` manually set as False
        )

        # This time, it shouldn't be there at all.
        html = render_crispy_form(test_form)
        assert (
            html.count('<div id="one" class="accordion-collapse %s"' % accordion_class)
            == 0
        )

    @override_settings(CRISPY_CLASS_CONVERTERS=CONVERTERS)
    def test_bs5accordion(self):
        random.seed(0)
        form = SampleForm()
        form.helper = FormHelper()
        form.helper.form_tag = False
        form.helper.layout = Layout(
            BS5Accordion(
                AccordionGroup("one", "first_name"),
                AccordionGroup("two", "password1", "password2"),
            )
        )
        assert parse_form(form) == parse_expected("accordion.html")

    def test_bs5accordion_active_false_not_rendered(self):
        test_form = SampleForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(
            BS5Accordion(
                AccordionGroup("one", "first_name"),
                # there is no ``active`` kwarg here.
            )
        )

        # The first time, there should be one of them there.
        html = render_crispy_form(test_form)

        accordion_class = "collapse show"

        assert (
            html.count('<div id="one" class="accordion-collapse %s"' % accordion_class)
            == 1
        )

        test_form.helper.layout = Layout(
            BS5Accordion(
                AccordionGroup("one", "first_name", active=False),
            )  # now ``active`` manually set as False
        )

        # This time, it shouldn't be there at all.
        html = render_crispy_form(test_form)
        assert (
            html.count('<div id="one" class="accordion-collapse %s"' % accordion_class)
            == 0
        )

    @override_settings(CRISPY_CLASS_CONVERTERS=CONVERTERS)
    def test_bs5accordion_flush(self):
        random.seed(0)
        test_form = SampleForm()
        test_form.helper = FormHelper()
        test_form.helper.form_tag = False
        test_form.helper.layout = Layout(
            BS5Accordion(
                AccordionGroup("one", "first_name"),
                AccordionGroup("two", "password1", "password2"),
                flush=True,
            )
        )
        assert parse_form(test_form) == parse_expected("accordion_flush.html")

    @override_settings(CRISPY_CLASS_CONVERTERS=CONVERTERS)
    def test_bs5accordion_always_open(self):
        random.seed(0)
        test_form = SampleForm()
        test_form.helper = FormHelper()
        test_form.helper.form_tag = False
        test_form.helper.layout = Layout(
            BS5Accordion(
                AccordionGroup("one", "first_name"),
                AccordionGroup("two", "password1", "password2"),
                always_open=True,
            )
        )
        assert parse_form(test_form) == parse_expected("accordion_always_open.html")

    def test_alert(self):
        test_form = SampleForm()
        test_form.helper = FormHelper()
        test_form.helper.form_tag = False
        test_form.helper.layout = Layout(
            Alert(content="Testing...", css_class="alert-primary"),
            Alert(content="Testing...", css_class="alert-primary", dismiss=False),
        )
        assert parse_form(test_form) == parse_expected("alert.html")

    def test_tab_and_tab_holder(self):
        test_form = SampleForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(
            TabHolder(
                Tab(
                    "one",
                    "first_name",
                    css_id="custom-name",
                    css_class="first-tab-class active",
                ),
                Tab("two", "password1", "password2"),
            )
        )
        html = render_crispy_form(test_form)

        assert (
            html.count(
                '<ul class="nav nav-tabs"> <li class="nav-item">'
                '<a class="nav-link active" href="#custom-name" data-bs-toggle="tab">'
                "One</a></li>"
            )
            == 1
        )
        assert html.count("tab-pane") == 2

        assert html.count('class="tab-pane first-tab-class active"') == 1

        assert html.count('<div id="custom-name"') == 1
        assert html.count('<div id="two"') == 1
        assert html.count('name="first_name"') == 1
        assert html.count('name="password1"') == 1
        assert html.count('name="password2"') == 1

    def test_tab_helper_reuse(self):
        # this is a proper form, according to the docs.
        # note that the helper is a class property here,
        # shared between all instances
        class SampleForm(forms.Form):
            val1 = forms.CharField(required=False)
            val2 = forms.CharField(required=True)
            helper = FormHelper()
            helper.layout = Layout(
                TabHolder(
                    Tab("one", "val1"),
                    Tab("two", "val2"),
                )
            )

        # first render of form => everything is fine
        test_form = SampleForm()
        html = render_crispy_form(test_form)

        # second render of form => first tab should be active,
        # but not duplicate class
        test_form = SampleForm()
        html = render_crispy_form(test_form)
        assert html.count('class="nav-item active active"') == 0

        # render a new form, now with errors
        test_form = SampleForm(data={"val1": "foo"})
        html = render_crispy_form(test_form)
        tab_class = "tab-pane"
        # if settings.CRISPY_TEMPLATE_PACK == 'bootstrap4':
        # tab_class = 'nav-link'
        # else:
        # tab_class = 'tab-pane'
        # tab 1 should not be active
        assert html.count('<div id="one" \n    class="{} active'.format(tab_class)) == 0
        # tab 2 should be active
        assert html.count('<div id="two" \n    class="{} active'.format(tab_class)) == 1

    def test_radio_attrs(self):
        form = CheckboxesSampleForm()
        form.fields["inline_radios"].widget.attrs = {"class": "first"}
        form.fields["checkboxes"].widget.attrs = {"class": "second"}
        html = render_crispy_form(form)
        assert 'class="first"' in html
        assert 'class="second"' in html

    def test_field_with_buttons(self):
        form = SampleForm()
        form.helper = FormHelper()
        form.helper.layout = Layout(
            FieldWithButtons(
                Field("password1", css_class="span4"),
                StrictButton("Go!", css_id="go-button"),
                StrictButton("No!", css_class="extra"),
                StrictButton("Test", type="submit", name="whatever", value="something"),
                css_class="extra",
                autocomplete="off",
            )
        )
        html = render_crispy_form(form)

        form_group_class = "mb-3"

        assert html.count('class="%s extra"' % form_group_class) == 1
        assert html.count('autocomplete="off"') == 1
        assert html.count('class="span4') == 1
        assert html.count('id="go-button"') == 1
        assert html.count("Go!") == 1
        assert html.count("No!") == 1
        assert html.count('class="btn"') == 2
        assert html.count('class="btn extra"') == 1
        assert html.count('type="submit"') == 1
        assert html.count('name="whatever"') == 1
        assert html.count('value="something"') == 1

    def test_hidden_fields(self):
        form = SampleForm()
        # All fields hidden
        for field in form.fields:
            form.fields[field].widget = forms.HiddenInput()

        form.helper = FormHelper()
        form.helper.layout = Layout(
            AppendedText("password1", "foo"),
            PrependedText("password2", "bar"),
            PrependedAppendedText("email", "bar"),
            InlineCheckboxes("first_name"),
            InlineRadios("last_name"),
        )
        html = render_crispy_form(form)
        assert html.count("<input") == 5
        assert html.count('type="hidden"') == 5
        assert html.count("<label") == 0

    def test_multiplecheckboxes(self):
        test_form = CheckboxesSampleForm()
        html = render_crispy_form(test_form)
        assert html.count("checked") == 6

        test_form.helper = FormHelper(test_form)
        test_form.helper[1].wrap(InlineCheckboxes, inline=True)
        html = render_crispy_form(test_form)
        # TODO Fix this test
        # assert html.count('form-check-input"') == 3

    def test_multiple_checkboxes_unique_ids(self):
        test_form = CheckboxesSampleForm()
        html = render_crispy_form(test_form)

        expected_ids = [
            "checkboxes_0",
            "checkboxes_1",
            "checkboxes_2",
            "alphacheckboxes_0",
            "alphacheckboxes_1",
            "alphacheckboxes_2",
            "numeric_multiple_checkboxes_0",
            "numeric_multiple_checkboxes_1",
            "numeric_multiple_checkboxes_2",
        ]
        for id_suffix in expected_ids:
            expected_str = f'id="id_{id_suffix}"'
            assert html.count(expected_str) == 1

    def test_inline_field(self):
        form = SampleForm()
        form.helper = FormHelper()
        form.helper.layout = Layout(
            InlineField("first_name", wrapper_class="col-4"),
            InlineField("is_company", wrapper_class="col-4"),
        )
        form.helper.form_class = "row row-cols-lg-auto align-items-center"
        assert parse_form(form) == parse_expected("test_inline_field.html")

    def test_float_field(self):
        form = SampleForm()
        form.helper = FormHelper()
        form.helper.layout = Layout(
            FloatingField("first_name"),
        )
        assert parse_form(form) == parse_expected("test_floating_field.html")

        form = InputsForm({})
        form.helper = FormHelper()
        form.helper.layout = Layout(
            FloatingField("text_area"),
            FloatingField("select_input"),
        )
        if django.VERSION < (5, 0):
            expected = "test_floating_field_failing_lt50.html"
        else:
            expected = "test_floating_field_failing.html"
        assert parse_form(form) == parse_expected(expected)

    def test_grouped_checkboxes_radios(self):
        form = GroupedChoiceForm()
        form.helper = FormHelper()
        form.helper.layout = Layout("checkbox_select_multiple")
        assert parse_form(form) == parse_expected("test_grouped_checkboxes.html")
        form.helper.layout = Layout("radio")
        assert parse_form(form) == parse_expected("test_grouped_radios.html")

        form = GroupedChoiceForm({})
        form.helper = FormHelper()
        form.helper.layout = Layout("checkbox_select_multiple")
        if django.VERSION < (5, 0):
            expected = "test_grouped_checkboxes_failing_lt50.html"
        else:
            expected = "test_grouped_checkboxes_failing.html"
        assert parse_form(form) == parse_expected(expected)

        form.helper.layout = Layout("radio")
        if django.VERSION < (5, 0):
            expected = "test_grouped_radios_failing_lt50.html"
        else:
            expected = "test_grouped_radios_failing.html"
        assert parse_form(form) == parse_expected(expected)

    def test_switch(self):
        form = SampleForm()
        form["is_company"].help_text = "is_company help text"
        form.helper = FormHelper()
        form.helper.layout = Layout(Switch("is_company"))
        assert parse_form(form) == parse_expected("test_switch.html")

    def test_switch_horizontal(self):
        form = SampleForm()
        form["is_company"].help_text = "is_company help text"
        form.helper = FormHelper()
        form.helper.label_class = "col-lg-2"
        form.helper.field_class = "col-lg-8"
        form.helper.form_class = "form-horizontal"
        form.helper.layout = Layout(Switch("is_company"), "first_name")
        assert parse_form(form) == parse_expected("test_switch_horizontal.html")

    def test_modal(self):
        test_form = SampleForm()
        test_form.helper = FormHelper()
        test_form.helper.form_tag = False
        test_form.helper.layout = Layout(
            Modal(
                'field1',
                css_id="modal-id-ex",
                css_class="modal-class-ex",
                title="This is my modal",
            )
        )
        assert parse_form(test_form) == parse_expected("modal.html")

    def test_inline_checkboxes(self):
        form = CheckboxesSampleForm()
        form.helper = FormHelper()
        form.helper.layout = InlineRadios("checkboxes")
        assert parse_form(form) == parse_expected("inline_checkboxes.html")
