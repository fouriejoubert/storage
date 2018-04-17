from django.urls import path, re_path
from django.conf.urls import include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu', views.menu, name='menu'),
    path('all_entries', views.all_entries, name='all_entries'),
    path('show_users_in_group_latest/', views.show_users_in_group_latest, name='show_users_in_group_latest'),
    path('choose_group_for_display/', views.choose_group_for_display, name='choose_group_for_display'),
    path('display_group/<int:group_id>/', views.display_group, name='display_group'),
    ]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

