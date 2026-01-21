from django.urls import path

from mailing_app.apps import MailingAppConfig
from mailing_app.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, \
    MailingDeleteView, start_mailing

app_name = MailingAppConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='mailings_list'),
    path('mailing_item/<int:pk>/', MailingDetailView.as_view(), name='mailing_item'),
    path('new/', MailingCreateView.as_view(), name='mailing_create'),
    path('<int:pk>/edit/', MailingUpdateView.as_view(), name='mailing_form'),
    path('<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('<int:pk>/start/', start_mailing, name='start_mailing'),
]
