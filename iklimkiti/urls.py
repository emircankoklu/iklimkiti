from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import admin_cop31_guide, custom_404

urlpatterns = [
    path('', include('core.urls')),
    path('konular/', include('learning.urls')),
    path('oyunlar/', include('games.urls')),
    path('profil/', include('accounts.urls')),
    path('admin/cop31-briefing-7f3c/', admin_cop31_guide, name='admin_cop31_guide'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = custom_404
