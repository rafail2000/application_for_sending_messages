from django.contrib import admin

from mailing_app.models import MailingRecipient, Message, Mailing, MailingAttempts


@admin.register(MailingRecipient)
class MailingRecipientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'initials', 'comment',)
    list_filter = ('initials',)
    search_fields = ('email', 'initials',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'letter_subject', 'letter_body',)
    list_filter = ('id',)
    search_fields = ('letter_subject', 'letter_body',)

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time', 'status',)
    list_filter = ('id',)
    search_fields = ('status', 'message', 'recipients')

@admin.register(MailingAttempts)
class MailingAttemptsAdmin(admin.ModelAdmin):
    list_display = ('id', 'attempt_time', 'status', 'server_response',)
    list_filter = ('id',)
    search_fields = ('status', 'server_response', 'mailing')
