from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from mailing_app.models import Message


class MessageCreateView(CreateView):
    """
    Курсор для создания сообщений
    """

    model = Message
    template_name = 'mailing_app/message_form.html'
    success_url = reverse_lazy('mailing_app/message_list.html')


class MessageListView(ListView):
    """
    Курсор для просмотра списка сообщений
    """

    model = Message
    template_name = 'mailing_app/messages_list.html'
    context_object_name = 'messages'


class MessageDetailView(DetailView):
    """
    Курсор для просмотра сообщения
    """

    model = Message
    template_name = 'mailing_app/message_detail.html'
    context_object_name = 'message'


class MessageUpdateView(UpdateView):
    """
    Курсор для обновления сообщения
    """

    model = Message
    template_name = 'mailing_app/message_forml.html'
    success_url = reverse_lazy('mailing_app/message_list.html')


class MessageDeleteView(DetailView):
    """
    Курсор для удаления сообщения
    """

    model = Message
    template_name = 'mailing_app/message_confirm_delete.html'
    success_url = reverse_lazy('mailing_app/message_list.html')
