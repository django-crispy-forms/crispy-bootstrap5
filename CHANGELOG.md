# CHANGELOG FOR CRISPY-BOOTSTRAP5

## Next Release
* Added Python 3.13 support. 
* Added support for Django 5.2. This required the following template changes:
  * Added `aria-describedby` to `<fieldset>` elements.
  * Added a parent `<div>` for errors to allow them to be referenced by `aria-describedby`. This means error messages can now be read by screen reader users.

## 2024.10 (2024-10-05)
* Added support for Django 5.1.
* Fixed `accordion.html`, `accordion-group.html` and `tab.html` templates to render `css_class` attribute.
* Dropped support for django-crispy-forms 2.2 and earlier.
* FormActions template improvements. The template now considers the `css_class` argument and adds the `row` class for Horizontal forms.

## 2024.2 (2024-02-24)

* Added support for [Switches](https://getbootstrap.com/docs/5.2/forms/checks-radios/#switches). (#162)
* Used `<fieldset>` and `<legend>` to group related inputs.
* Added modal template.

## 2023.10 (2023-10-2023)
* Added Django 5.0 and 4.2 support
* Added Python 3.11 and 3.12 support
* Dropped Python 3.7 support
* Dropped Django 3.2, 4.0 and 4.1 support
* Switched to CalVer versioning

See [Milestones](https://github.com/django-crispy-forms/crispy-bootstrap5/milestone/8?closed=1) for full change log.

## 0.7 (2022-09-28)
* Added Django 4.1 support

See [Milestones](https://github.com/django-crispy-forms/crispy-bootstrap5/milestones?state=closed) for for change list.

## 0.6 (2021-09-28)
* Added Django 4.0 support

## 0.5 (2021-08-20)
* Added support for [Accordion Flush](https://getbootstrap.com/docs/5.0/components/accordion/#flush) and 
  [Always Open](https://getbootstrap.com/docs/5.0/components/accordion/#always-open) (#63)
* Added support for grouped inputs (#64)
* Added support for clearable file field (#53)
* Removed various `|safe` filters in templates

See [Milestones](https://github.com/django-crispy-forms/crispy-bootstrap5/milestone/6?closed=1) for full changelog.


## 0.4 (2021-05-27)
* Added support for Bootstrap 5 Floating Labels (#42)
* Dropped support for Django 3.0
* Added support for Django 3.2

See [Milestones](https://github.com/django-crispy-forms/crispy-bootstrap5/milestone/5?closed=1) for full changelog.

## 0.3.1(2021-03-03)
* Fixed classes for `row` layout object (#36)

See [Milestones](https://github.com/django-crispy-forms/crispy-bootstrap5/milestone/4?closed=1) for full changelog.

## 0.3 (2021-02-21)
* Fixed rendering of select widgets (#31)

See [Milestones](https://github.com/django-crispy-forms/crispy-bootstrap5/milestone/3?closed=1) for full changelog.

## 0.2 (2021-01-31)
* Tested for compatibility with Bootstrap5 Beta 1
* Fixed InlineField (#28)
* Implemented new Bootstrap5 accordion (#24)
* Improved tests and fixed rendering of blank attributes (#23) 

See [Milestones](https://github.com/django-crispy-forms/crispy-bootstrap5/milestone/2) for full changelog.

## 0.1 (2020-11-19)
* Initial release, compatibility with Bootstrap5 Alpha 3
* Converted templates from Bootstrap 4, and initial set of fixes
* Brought forward Bootstrap 4 test suite and updated for Bootstrap5

See [Milestones](https://github.com/django-crispy-forms/crispy-bootstrap5/milestone/1) for full changelog. 
