from django.contrib import admin

from core.models import GuideSection, HomeAction, HomePageContent, IdeathonGuide


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
