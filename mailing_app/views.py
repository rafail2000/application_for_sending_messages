from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from mailing_app.models import Message, Mailing


class MailingCreateView(CreateView):
    """
    Курсор для создания рассылки
    """

    model = Mailing
    template_name = 'mailing_app/mailing_form.html'
    success_url = reverse_lazy('mailing_app/mailing_form.html')


class MailingListView(ListView):
    """
    Курсор для просмотра списка рассылок
    """

    model = Mailing
    template_name = 'mailing_app/mailings_list.html'
    context_object_name = 'mailings'


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
    template_name = 'mailing_app/mailing_forml.html'
    success_url = reverse_lazy('mailing_app/mailing_list.html')


class MailingDeleteView(DetailView):
    """
    Курсор для удаления рассылки
    """

    model = Mailing
    template_name = 'mailing_app/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_app/message_list.html')
