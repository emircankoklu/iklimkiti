from django.urls import path

from accounts.views import login_view, logout_view, register_view
from core.views import (
    about, assistant_view, chatbot_api, digital_missions, home, invoice_analysis_api,
    invoice_analysis_view, references,
)

urlpatterns = [
    path('', home, name='home'),
    path('dijital-gorevler/', digital_missions, name='digital_missions'),
    path('hakkimizda/', about, name='about'),
    path('kaynakca/', references, name='references'),
    path('asistan/', assistant_view, name='assistant'),
    path('fatura-analizi/', invoice_analysis_view, name='invoice_analysis'),
    path('api/fatura-analizi/', invoice_analysis_api, name='invoice_analysis_api'),
    path('api/chatbot/', chatbot_api, name='chatbot_api'),
    path('accounts/login/', login_view, name='legacy_login'),
    path('kayit/', register_view, name='register'),
    path('giris/', login_view, name='login'),
    path('cikis/', logout_view, name='logout'),
]
