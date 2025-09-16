from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from tutorial.quickstart import views_tutorial3_generic as views

urlpatterns = [
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('groups/', views.GroupList.as_view(), name='group-list'),
    path('groups/<int:pk>/', views.GroupDetail.as_view(), name='group-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
