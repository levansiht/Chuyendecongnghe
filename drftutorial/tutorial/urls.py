from django.urls import include, path
from rest_framework import routers

from tutorial.quickstart import views

# Original ViewSet-based routing (Tutorial 1)
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Tutorial 2: Function-based views with format suffixes
from tutorial.urls_tutorial2 import urlpatterns as tutorial2_patterns

# Tutorial 3: Class-based views
from tutorial.urls_tutorial3_apiview import urlpatterns as tutorial3_apiview_patterns
from tutorial.urls_tutorial3_mixins import urlpatterns as tutorial3_mixins_patterns
from tutorial.urls_tutorial3_generic import urlpatterns as tutorial3_generic_patterns

# Tutorial 4: Authentication & Permissions
from tutorial.urls_tutorial4 import urlpatterns as tutorial4_patterns

# Tutorial 5: Hyperlinked APIs
from tutorial.urls_tutorial5 import urlpatterns as tutorial5_patterns

# Tutorial 6: ViewSets & Routers
from tutorial.urls_tutorial6 import urlpatterns as tutorial6_patterns

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # Tutorial 1 - ViewSets with router
    path('v1/', include(router.urls)),
    
    # Tutorial 2 - Function-based views with format suffixes
    path('v2/', include(tutorial2_patterns)),
    
    # Tutorial 3 - Class-based views (APIView)
    path('v3a/', include(tutorial3_apiview_patterns)),
    
    # Tutorial 3 - Class-based views (Mixins)
    path('v3b/', include(tutorial3_mixins_patterns)),
    
    # Tutorial 3 - Class-based views (Generic)
    path('v3c/', include(tutorial3_generic_patterns)),
    
    # Tutorial 4 - Authentication & Permissions
    path('v4/', include(tutorial4_patterns)),
    
    # Tutorial 5 - Hyperlinked APIs
    path('v5/', include(tutorial5_patterns)),
    
    # Tutorial 6 - ViewSets & Routers
    path('v6/', include(tutorial6_patterns)),
    
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
