from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tutorial.quickstart import views_tutorial6 as views

# Create a router and register our ViewSets with it
router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'users', views.UserViewSet, basename='user') 
router.register(r'groups', views.GroupViewSet, basename='group')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
