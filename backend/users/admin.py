from django.contrib import admin

from .models import User, NotConfirmedEmail, UserBalance


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('registration_date',)

    exclude = ('password', 'last_login')
    prepopulated_fields = {
        'slug': ('username',)
    }
    list_display = ('first_name', 'surname', 'username', 'email', 'is_superuser')
    list_filter = ('is_activated', 'is_superuser')
    search_fields = ('first_name', 'surname', 'username', 'email')
    ordering = ('first_name', 'surname', 'username', 'email')


@admin.register(NotConfirmedEmail)
class NotConfirmedEmailAdmin(admin.ModelAdmin):
    list_display = ('user', 'email',)


@admin.register(UserBalance)
class UserBalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'coins_amount',)
