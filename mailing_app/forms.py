from django.forms import BooleanField, ModelForm

from mailing_app.models import Mailing, MailingRecipient, Message


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


class MailingRecipientForm(StyleFormMixin, ModelForm):
    """
    Класс формы получателя рассылки
    """

    class Meta:
        model = MailingRecipient
        fields = '__all__'


class MessageForm(StyleFormMixin, ModelForm):
    """
    Класс формы сообщения
    """

    class Meta:
        model = Message
        fields = '__all__'


class MailingForm(StyleFormMixin, ModelForm):
    """
    Класс формы рассылки
    """

    class Meta:
        model = Mailing
        fields = '__all__'
        exclude = ('is_published',)


class MailingManagerForm(StyleFormMixin, ModelForm):
    """
    Класс формы рассылки для модератора
    """

    class Meta:
        model = Mailing
        fields = '__all__'
