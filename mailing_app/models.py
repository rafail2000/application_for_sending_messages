from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from users.models import User


class MailingRecipient(models.Model):
    """
    Модель получателя рассылки
    """

    email = models.EmailField(unique=True, verbose_name="Email")
    initials = models.CharField(
        max_length=255, verbose_name="Ф.И.О.", help_text="Введите вашу фамилию, имя и отчество"
    )
    comment = models.TextField(verbose_name="комментарий", help_text="Введите комментарий")

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        permissions = [
            ('can_unpublish_product', 'Can unpublished product'),
        ]

    def __str__(self):
        return self.initials


class Message(models.Model):
    """
    Модель сообщение
    """

    letter_subject = models.CharField(max_length=255, verbose_name="Тема письма", help_text="Введите тему письма")
    letter_body = models.TextField(verbose_name="Тело письма", help_text="Введите тело письма")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.letter_body


class Mailing(models.Model):
    """
    Модель рассылка
    """

    start_time = models.DateTimeField(
        verbose_name="Дата и время начала отправки", help_text="Введите дату и время начала отправки"
    )
    end_time = models.DateTimeField(
        verbose_name="Дата и время окончания отправки", help_text="Введите дату и время окончания отправки"
    )
    status = models.CharField(max_length=20, default="Создана", verbose_name="Статус рассылки")
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(MailingRecipient)
    owner = models.ForeignKey(
        User,
        verbose_name='Владелец',
        help_text='Укажите имя владельца',
        blank=True,
        null=True,
        on_delete=models.SET_NULL)

    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликовано'
    )


    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ('can_unpublish_product', 'Can unpublished product'),
        ]

    def __str__(self):
        return self.status

    def clean(self):
        """
        Валидация даты в модели
        """

        validate_errors = {}

        if self.start_time is not None:
            if self.start_time < timezone.now():
                validate_errors["start_time"] = "Время начала не может быть в прошлом"
        else:
            validate_errors["start_time"] = "Укажите время начало"

        if self.start_time is not None and self.end_time is not None:
            if self.start_time > self.end_time:
                validate_errors["end_time"] = "Время окончания не может быть раньше времени начала"

        if self.end_time is None:
            validate_errors["end_time"] = "Укажите время окончания"

        if validate_errors:
            raise ValidationError(validate_errors)

    def update_status(self) -> str:
        """
        Метод для обновления статуса рассылки
        """

        now = timezone.now()

        if now < self.start_time:
            new_status = "Создана"
        elif self.start_time <= now <= self.end_time:
            new_status = "Запущена"
        else:
            new_status = "Завершена"

        self.status = new_status

        self.save(update_fields=["status"])
        return new_status


class MailingAttempts(models.Model):
    """
    Модель попыток рассылок
    """

    attempt_time = models.DateTimeField(
        verbose_name="Дата и время попытки отправки", help_text="Введите дату и время попытки отправки"
    )
    status = models.CharField(max_length=20, verbose_name="статус", help_text="введите статус")
    server_response = models.TextField(verbose_name="Ответ сервера", help_text="Введите ответ сервера")
    mailing = models.ForeignKey(Message, on_delete=models.CASCADE)
