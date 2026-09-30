from django.contrib import admin

from games.models import GameAttempt, GameProgress, MiniGame


@admin.register(MiniGame)
class MiniGameAdmin(admin.ModelAdmin):
	list_display = ('title', 'topic', 'game_type', 'difficulty', 'status', 'is_published', 'updated_at')
	list_filter = ('status', 'game_type', 'difficulty', 'is_published', 'topic')
	search_fields = ('title', 'description', 'instructions', 'topic__title')
	autocomplete_fields = ('topic',)
	prepopulated_fields = {'slug': ('title',)}
	list_editable = ('status', 'is_published')
	fieldsets = (
		('Oyun bilgileri', {'fields': ('topic', 'title', 'slug', 'description', 'instructions')}),
		('Oyun ayarları', {'fields': ('game_type', 'difficulty', 'estimated_duration_seconds', 'thumbnail', 'configuration_json')}),
		('Yayın', {'fields': ('status', 'is_published')}),
	)


@admin.register(GameProgress)
class GameProgressAdmin(admin.ModelAdmin):
	list_display = ('user', 'game', 'status', 'score', 'attempts_count', 'last_played_at')
	list_filter = ('status', 'game')
	search_fields = ('user__username', 'game__title')
	autocomplete_fields = ('user', 'game')
	readonly_fields = ('created_at', 'updated_at', 'last_played_at')


@admin.register(GameAttempt)
class GameAttemptAdmin(admin.ModelAdmin):
	list_display = ('user', 'game', 'score', 'passed', 'created_at')
	list_filter = ('passed', 'game')
	search_fields = ('user__username', 'game__title')
	autocomplete_fields = ('user', 'game')
	readonly_fields = ('created_at',)
