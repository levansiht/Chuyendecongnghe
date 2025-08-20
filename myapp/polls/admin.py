from django.contrib import admin
from .models import Question, Choice, Person, Category, Post

# Register your models here.


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'question', 'votes')
    list_filter = ['question']
    search_fields = ['choice_text']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'birth_date', 'created_at')
    list_filter = ['created_at', 'birth_date']
    search_fields = ['first_name', 'last_name', 'email']
    ordering = ['last_name', 'first_name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ['name']
    ordering = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'published', 'created_at')
    list_filter = ['published', 'created_at', 'category']
    search_fields = ['title', 'content']
    ordering = ['-created_at']
