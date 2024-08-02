from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from calendario.views import *
from calendario import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('', TemplateView.as_view(template_name="calendarioBase.html"), name='calendarioBase'),
    path('calendario/', calendario, name='calendario'),
    path('calendario/novo_evento/', CalenadarioNovo_evento, name='novo_evento'),
    path('calendario/detalhes/<int:id>/', calendario_detalhes, name='detalhes'),
    path('calendario/calendarioResponsavel', calendario, name='calendarioResponsavel'),
    path('calendario/CalendarioEdit/<int:id>/', CalendarioEdit, name='CalendarioEdit'),
    path('calendario/CalendarioConcluido/<int:id>/', CalendarioConcluido, name='CalendarioConcluido'),
    path('calendario/CalendarioExluido/<int:id>/', CalendarioDelete, name='removeCalendario'),
    path('calendario/observacao/<int:id>/', CalendarioEdit, name='observacao'),
    path('senha/', auth_views.PasswordChangeView.as_view(), name='mudarSenha')

]
