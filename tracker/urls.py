from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('setup/', views.character_setup, name='character_setup'),
    path('stats/', views.stats_view, name='stats'),
    path('history/', views.history_view, name='history'),
    path('achievements/', views.achievements_view, name='achievements'),
    path('settings/', views.settings_view, name='settings'),
    path('api/complete_task/', views.complete_task_api, name='complete_task_api'),
    path('api/day_detail/<int:log_id>/', views.day_detail_api, name='day_detail_api'),
]
