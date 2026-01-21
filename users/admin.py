from django.contrib import admin

from users.models import User


@admin.register(User)
class BookAdmin(admin.ModelAdmin):
    list_display = ('email', 'avatar', 'phone', 'country')
    list_filter = ('email',)
