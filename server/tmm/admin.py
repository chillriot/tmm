from django.contrib import admin

from .models import UserMails


@admin.register(UserMails)
class UserMailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'date_added')