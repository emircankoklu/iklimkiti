from django.contrib import admin

from learning.models import (
	GlossaryTerm,
	InformationCard,
	LessonModule,
	MindMap,
	MindMapNode,
	QuestionAnswer,
	Source,
	Topic,
	VideoContent,
)


class LessonModuleInline(admin.TabularInline):
	model = LessonModule
	extra = 0
	fields = ('title', 'order', 'is_published')


class InformationCardInline(admin.StackedInline):
	model = InformationCard
	extra = 0
	fields = ('title', 'card_type', 'content', 'is_published')


class QuestionAnswerInline(admin.StackedInline):
	model = QuestionAnswer
	extra = 0
	fields = ('order', 'question', 'answer', 'score_dimension', 'is_published')


class MindMapNodeInline(admin.TabularInline):
	model = MindMapNode
	extra = 1


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
	list_display = ('title', 'theme', 'order', 'is_published', 'updated_at')
	list_display_links = ('title',)
	list_editable = ('order', 'is_published')
	list_filter = ('is_published', 'theme')
	search_fields = ('title', 'description', 'theme', 'key_question')
	prepopulated_fields = {'slug': ('title',)}
	inlines = (LessonModuleInline, InformationCardInline, QuestionAnswerInline)
	fieldsets = (
		('Temel bilgiler', {'fields': ('title', 'slug', 'theme', 'description')}),
		('Öğrenciye gösterilecek yönlendirme', {'fields': ('key_question', 'action_text', 'target_age', 'estimated_duration_minutes')}),
		('Yayın', {'fields': ('order', 'is_published')}),
	)


@admin.register(LessonModule)
class LessonModuleAdmin(admin.ModelAdmin):
	list_display = ('title', 'topic', 'order', 'is_published')
	list_filter = ('is_published', 'topic')
	search_fields = ('title', 'description', 'problem_statement', 'topic__title')
	autocomplete_fields = ('topic',)
	prepopulated_fields = {'slug': ('title',)}
	fieldsets = (
		('Modül', {'fields': ('topic', 'title', 'slug', 'order', 'is_published')}),
		('Ders içeriği', {'fields': ('description', 'problem_statement', 'real_life_example', 'action_challenge')}),
	)


@admin.register(InformationCard)
class InformationCardAdmin(admin.ModelAdmin):
	list_display = ('title', 'topic', 'card_type', 'is_published')
	list_filter = ('card_type', 'is_published', 'topic')
	search_fields = ('title', 'content', 'topic__title')
	autocomplete_fields = ('topic',)


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
	list_display = ('question', 'topic', 'score_dimension', 'order', 'is_published')
	list_display_links = ('question',)
	list_filter = ('is_published', 'score_dimension', 'topic')
	search_fields = ('question', 'answer', 'topic__title')
	autocomplete_fields = ('topic',)
	list_editable = ('order', 'is_published')


@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
	list_display = ('title', 'topic', 'is_published', 'created_at')
	list_filter = ('is_published', 'topic')
	search_fields = ('title', 'description', 'topic__title')
	autocomplete_fields = ('topic',)
	prepopulated_fields = {'slug': ('title',)}


@admin.register(MindMap)
class MindMapAdmin(admin.ModelAdmin):
	list_display = ('title', 'topic', 'is_published', 'created_at')
	list_filter = ('is_published', 'topic')
	search_fields = ('title', 'description', 'topic__title')
	autocomplete_fields = ('topic',)
	prepopulated_fields = {'slug': ('title',)}
	inlines = (MindMapNodeInline,)


@admin.register(GlossaryTerm)
class GlossaryTermAdmin(admin.ModelAdmin):
	list_display = ('title', 'related_topic', 'is_published', 'created_at')
	list_filter = ('is_published', 'related_topic')
	search_fields = ('title', 'definition', 'related_topic__title')
	autocomplete_fields = ('related_topic',)
	prepopulated_fields = {'slug': ('title',)}


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
	list_display = ('title', 'organization', 'source_type', 'is_verified')
	list_filter = ('source_type', 'is_verified')
	search_fields = ('title', 'organization', 'description')
	list_editable = ('is_verified',)
