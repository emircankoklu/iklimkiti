from django.contrib import admin

from accounts.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('display_name', 'user', 'created_at', 'updated_at')
	search_fields = ('display_name', 'user__username', 'user__email')
	autocomplete_fields = ('user',)
