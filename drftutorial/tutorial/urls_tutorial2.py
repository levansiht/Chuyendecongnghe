from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from tutorial.quickstart import views_tutorial2 as views

urlpatterns = [
    path('users/', views.user_list, name='user-list'),
    path('users/<int:pk>/', views.user_detail, name='user-detail'),
    path('groups/', views.group_list, name='group-list'),
    path('groups/<int:pk>/', views.group_detail, name='group-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
