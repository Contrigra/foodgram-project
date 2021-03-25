from django.contrib import admin
from django.contrib.auth import get_user_model


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'email',)
    list_display = ('pk', 'username', 'last_login', 'date_joined',)
    list_filter = ('last_login', 'email',)
    readonly_fields = ['last_login', 'date_joined', ]
    empty_value_display = '-empty-'
