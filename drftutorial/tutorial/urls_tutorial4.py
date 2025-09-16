from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from tutorial.quickstart import views_tutorial4 as views

urlpatterns = [
    # Post endpoints (with ownership)
    path('posts/', views.PostList.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
    
    # User endpoints (read-only with relationships)
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('me/', views.current_user, name='current-user'),
    
    # Group endpoints (admin only)
    path('groups/', views.GroupList.as_view(), name='group-list'),
    path('groups/<int:pk>/', views.GroupDetail.as_view(), name='group-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
