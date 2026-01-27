from django.urls import path
from django.views.decorators.cache import cache_page

from mailing_app.apps import MailingAppConfig
from mailing_app.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, \
    MailingDeleteView, start_mailing, MailingRecipientCreateView, MailingRecipientListView, MailingRecipientUpdateView, \
    MailingRecipientDetailView, MailingRecipientDeleteView

app_name = MailingAppConfig.name

urlpatterns = [
    # Получатели рассылок
    path('recipients', MailingRecipientListView.as_view(), name='recipients_list'),
    path('recipients/<int:pk>/', cache_page(60 * 15)(MailingRecipientDetailView.as_view()), name='recipient_item'),
    path('recipients/new/', MailingRecipientCreateView.as_view(), name='recipient_create'),
    path('recipients<int:pk>/edit/', MailingRecipientUpdateView.as_view(), name='recipient_form'),
    path('recipients<int:pk>/delete/', MailingRecipientDeleteView.as_view(), name='recipient_delete'),

    # Рассылки
    path('', MailingListView.as_view(), name='mailings_list'),
    path('mailing_item/<int:pk>/', cache_page(60 * 15)(MailingDetailView.as_view()), name='mailing_item'),
    path('new/', MailingCreateView.as_view(), name='mailing_create'),
    path('<int:pk>/edit/', MailingUpdateView.as_view(), name='mailing_form'),
    path('<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('<int:pk>/start/', start_mailing, name='start_mailing'),
]
