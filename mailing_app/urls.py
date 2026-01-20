from django.urls import path

from mailing_app.apps import MailingAppConfig
from mailing_app.views import MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, \
    MessageDeleteView


app_name = MailingAppConfig.name

urlpatterns = [
    path('', MessageListView.as_view(), name='messages_list'),
    path('message_item/<int:pk>/', MessageDetailView.as_view(), name='message_item'),
    path('new/', MessageCreateView.as_view(), name='message_create'),
    path('<int:pk>/edit/', MessageUpdateView.as_view(), name='message_edit'),
    path('<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
]
