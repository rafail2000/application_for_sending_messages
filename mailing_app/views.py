from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .services import send_mail_recipients

from mailing_app.forms import MailingForm
from mailing_app.models import Mailing


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

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()  # ← пересчёт и сохранение статуса
        return obj


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


class MailingDeleteView(DeleteView):
    """
    Курсор для удаления рассылки
    """

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