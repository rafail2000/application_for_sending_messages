from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .services import send_mail_recipients, get_products_from_cache, get_recipients_from_cache, get_messages_from_cache

from mailing_app.forms import MailingForm, MailingManagerForm, MailingRecipientForm, MessageForm
from mailing_app.models import Mailing, MailingRecipient, Message


# Курсоры получателя рассылок
class MailingRecipientCreateView(CreateView):
    """
    Курсор для создания получателя рассылок
    """

    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = 'mailing_app/recipient_form.html'
    success_url = reverse_lazy('mailing_app:recipients_list')


class MailingRecipientListView(ListView):
    """
    Курсор для просмотра списка получателя рассылок
    """

    model = MailingRecipient
    template_name = 'mailing_app/recipients_list.html'
    context_object_name = 'recipients'

    def get_queryset(self):
        return get_recipients_from_cache().filter()


class MailingRecipientDetailView(DetailView):
    """
    Курсор для просмотра получателя рассылки
    """

    model = MailingRecipient
    template_name = 'mailing_app/recipient_item.html'
    context_object_name = 'recipient'


class MailingRecipientUpdateView(UpdateView):
    """
    Курсор для редактирования получателя рассылки
    """

    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = 'mailing_app/recipient_form.html'
    success_url = reverse_lazy('mailing_app:recipients_list')


class MailingRecipientDeleteView(DeleteView):
    """
    Курсор для удаления рассылки
    """

    model = MailingRecipient
    template_name = 'mailing_app/recipient_confirm_delete.html'
    success_url = reverse_lazy('mailing_app:recipients_list')


# Курсоры сообщения
class MessageCreateView(CreateView):
    """
    Курсор для создания сообщения
    """

    model = Message
    form_class = MessageForm
    template_name = 'mailing_app/message_form.html'
    success_url = reverse_lazy('mailing_app:messages_list')


class MessageListView(ListView):
    """
    Курсор для просмотра списка сообщений
    """

    model = Message
    template_name = 'mailing_app/messages_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return get_messages_from_cache().filter()


class MessageDetailView(DetailView):
    """
    Курсор для просмотра сообщения
    """

    model = Message
    template_name = 'mailing_app/message_item.html'
    context_object_name = 'message'


class MessageUpdateView(UpdateView):
    """
    Курсор для редактирования сообщения
    """

    model = Message
    form_class = MessageForm
    template_name = 'mailing_app/message_form.html'
    success_url = reverse_lazy('mailing_app:messages_list')


class MessageDeleteView(DeleteView):
    """
    Курсор для удаления сообщения
    """

    model = Message
    template_name = 'mailing_app/message_confirm_delete.html'
    success_url = reverse_lazy('mailing_app:messages_list')


# Курсоры рассылок
class MailingCreateView(CreateView):
    """
    Курсор для создания рассылки
    """

    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_app/mailing_form.html'
    success_url = reverse_lazy('mailing_app:mailings_list')


class MailingListView(ListView):
    """
    Курсор для просмотра списка рассылок
    """

    model = Mailing
    template_name = 'mailing_app/mailings_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        return get_products_from_cache().filter()

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = timezone.now()

        total_mailings = Mailing.objects.count()

        active_mailings = Mailing.objects.filter(
            start_time__lte=now,
            end_time__gte=now,
            status='Запущена'
        ).count()

        unique_recipients = MailingRecipient.objects.count()

        context.update({
            'total_mailings': total_mailings,
            'active_mailings': active_mailings,
            'unique_recipients': unique_recipients,
            'now': now,
        })

        return context


class MailingDetailView(DetailView):
    """
    Курсор для просмотра рассылки
    """

    model = Mailing
    template_name = 'mailing_app/mailing_item.html'
    context_object_name = 'mailing'


class MailingUpdateView(UpdateView):
    """
    Курсор для редактирования рассылки
    """

    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_app/mailing_form.html'
    success_url = reverse_lazy('mailing_app:mailings_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingForm
        if user.has_perm('mailing_app.can_unpublish_product'):
            return MailingManagerForm
        raise PermissionDenied


class MailingDeleteView(DeleteView):
    """
    Курсор для удаления рассылки
    """

    permission_required = ['catalog.delete_product']
    model = Mailing
    template_name = 'mailing_app/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_app:mailings_list')


@require_POST
def start_mailing(request, pk):
    """
    Контроллер для запуска рассылки по кнопке
    """

    mailing = get_object_or_404(Mailing, pk=pk)

    if mailing.status == "Запущена":
        messages.warning(request, f'Рассылка "{mailing}" уже запущена')
        return redirect('mailing_app:mailing_item', pk=pk)

    mailing.status = "Запущена"
    mailing.save(update_fields=['status'])

    try:

        result = send_mail_recipients(pk)

        messages.success(request, f'Рассылка "{mailing}" успешно запущена!')

    except Exception as e:
        messages.error(request, f'Ошибка при запуске рассылки: {str(e)}')
        # Возвращаем статус обратно в случае ошибки
        mailing.status = "Создана"
        mailing.save(update_fields=['status'])

    return redirect('mailing_app:mailing_item', pk=pk)