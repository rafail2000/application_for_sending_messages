from django.forms import BooleanField, ModelForm

from mailing_app.models import Message


class StyleFormMixin:
    """
    Класс Mixin для стилизации формы
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = "form-check-input"
            else:
                fild.widget.attrs['class'] = "form-control"


class MessageForm(StyleFormMixin, ModelForm):
    """
    Класс формы
    """

    class Meta:
        model = Message
        fields = '__all__'
