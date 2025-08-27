from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    # Function-based views
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/vote-ajax/', views.vote_ajax, name='vote_ajax'),
    
    # Class-based views
    path('questions/', views.QuestionListView.as_view(), name='question_list'),
    path('questions/<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('questions/create/', views.QuestionCreateView.as_view(), name='question_create'),
    path('questions/<int:pk>/edit/', views.QuestionUpdateView.as_view(), name='question_edit'),
    path('questions/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
    
    # Category views
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Statistics and API
    path('stats/', views.stats, name='stats'),
    path('api/questions/', views.api_questions, name='api_questions'),
]
