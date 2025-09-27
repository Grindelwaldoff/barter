from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class BootstrapFormMixin:

    input_class = "form-control"
    select_class = "form-select"
    checkbox_class = "form-check-input"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            self._apply_widget_classes(field.widget)

    def _apply_widget_classes(self, widget):
        class_map = {
            forms.CheckboxInput: self.checkbox_class,
            forms.Select: self.select_class,
            forms.SelectMultiple: self.select_class,
            forms.FileInput: self.input_class,
            forms.Textarea: self.input_class,
            forms.EmailInput: self.input_class,
            forms.NumberInput: self.input_class,
            forms.PasswordInput: self.input_class,
            forms.URLInput: self.input_class,
            forms.TextInput: self.input_class,
            forms.DateInput: self.input_class,
            forms.DateTimeInput: self.input_class,
            forms.TimeInput: self.input_class,
        }

        target_class = None
        for widget_type, css_class in class_map.items():
            if isinstance(widget, widget_type):
                target_class = css_class
                break

        input_type = getattr(widget, "input_type", None)
        if target_class and input_type != "hidden":
            existing = widget.attrs.get("class", "")
            if target_class not in existing.split():
                widget.attrs["class"] = f"{existing} {target_class}".strip()


class BootstrapAuthenticationForm(BootstrapFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = _("Логин")
        self.fields["password"].label = _("Пароль")
