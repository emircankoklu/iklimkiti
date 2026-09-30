from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect
from django.urls import path, reverse

from core.models import ChatPromptLog, GuideSection, HomeAction, HomePageContent, IdeathonGuide


@admin.register(ChatPromptLog)
class ChatPromptLogAdmin(admin.ModelAdmin):
	list_display = ('created_at', 'user', 'status')
	list_filter = ('status', 'created_at')
	search_fields = ('prompt', 'user__username')
	readonly_fields = ('user', 'prompt', 'status', 'created_at')
	date_hierarchy = 'created_at'

	def has_add_permission(self, request):
		return False

	def has_change_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def changelist_view(self, request, extra_context=None):
		extra_context = {**(extra_context or {}), 'can_clear_logs': request.user.is_superuser}
		return super().changelist_view(request, extra_context=extra_context)

	def get_urls(self):
		return [
			path(
				'clear-all/',
				self.admin_site.admin_view(self.clear_all_view),
				name='core_chatpromptlog_clear_all',
			),
		] + super().get_urls()

	def clear_all_view(self, request):
		if not request.user.is_superuser:
			raise PermissionDenied
		if request.method != 'POST':
			return HttpResponseNotAllowed(['POST'])
		deleted_count, _ = ChatPromptLog.objects.all().delete()
		self.message_user(request, f'{deleted_count} asistan log kaydı temizlendi.', messages.SUCCESS)
		return redirect(reverse('admin:core_chatpromptlog_changelist'))


class HomeActionInline(admin.TabularInline):
	model = HomeAction
	extra = 1
	fields = ('title', 'description', 'order', 'is_published')


@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
	fieldsets = (
		('Hero / ilk ekran', {'fields': ('hero_tag', 'hero_title', 'hero_description')}),
		('Gıda ve iklim bölümü', {'fields': ('relationship_title', 'relationship_lead', 'relationship_body')}),
		('Asistan bölümü', {'fields': ('assistant_title', 'assistant_description')}),
		('Yayın durumu', {'fields': ('is_active',)}),
	)
	inlines = (HomeActionInline,)
	readonly_fields = ('updated_at',)

	def has_add_permission(self, request):
		return not HomePageContent.objects.exists()


admin.site.register(HomeAction)


class GuideSectionInline(admin.StackedInline):
	model = GuideSection
	extra = 1
	fields = ('order', 'eyebrow', 'title', 'body', 'prompt', 'score_weight', 'is_published')


@admin.register(IdeathonGuide)
class IdeathonGuideAdmin(admin.ModelAdmin):
	fieldsets = (
		('Başlık ve kaynak', {'fields': ('title', 'subtitle', 'introduction', 'source_url')}),
		('Yayın', {'fields': ('is_published',)}),
	)
	inlines = (GuideSectionInline,)

	def has_add_permission(self, request):
		return not IdeathonGuide.objects.exists()


@admin.register(GuideSection)
class GuideSectionAdmin(admin.ModelAdmin):
	list_display = ('order', 'title', 'eyebrow', 'score_weight', 'is_published')
	list_display_links = ('title',)
	list_filter = ('is_published', 'eyebrow')
	search_fields = ('title', 'body', 'prompt')
	list_editable = ('order', 'score_weight', 'is_published')
admin.site.site_header = 'İklimKiti içerik yönetimi'
admin.site.site_title = 'İklimKiti yönetimi'
admin.site.index_title = 'İçerik merkezi'
