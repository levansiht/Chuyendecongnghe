from django.contrib import admin
from django.db.models import Count, Sum
from django.utils.html import format_html
from .models import Question, Choice, Category, Person, Article, Tag

# Register your models here.

class ChoiceInline(admin.TabularInline):
    """Inline admin for choices within question admin"""
    model = Choice
    extra = 2
    min_num = 2
    fields = ('choice_text', 'votes', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin configuration for Question model"""
    list_display = ('question_text', 'author', 'category', 'pub_date', 'is_active', 'choice_count', 'total_votes')
    list_filter = ('is_active', 'pub_date', 'category', 'author')
    search_fields = ('question_text', 'author__username', 'category__name')
    date_hierarchy = 'pub_date'
    list_per_page = 20
    
    fieldsets = (
        ('Question Information', {
            'fields': ('question_text', 'category', 'author', 'is_active')
        }),
        ('Publishing', {
            'fields': ('pub_date',),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ChoiceInline]
    
    def choice_count(self, obj):
        """Display number of choices for this question"""
        return obj.choices.count()
    choice_count.short_description = 'Choices'
    
    def total_votes(self, obj):
        """Display total votes for this question"""
        return obj.total_votes()
    total_votes.short_description = 'Total Votes'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related(
            'author', 'category'
        ).prefetch_related('choices')
    
    actions = ['make_active', 'make_inactive']
    
    def make_active(self, request, queryset):
        """Bulk action to make questions active"""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f'{updated} question(s) were successfully marked as active.'
        )
    make_active.short_description = 'Mark selected questions as active'
    
    def make_inactive(self, request, queryset):
        """Bulk action to make questions inactive"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated} question(s) were successfully marked as inactive.'
        )
    make_inactive.short_description = 'Mark selected questions as inactive'


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    """Admin configuration for Choice model"""
    list_display = ('choice_text', 'question', 'votes', 'vote_percentage', 'created_at')
    list_filter = ('created_at', 'question__category')
    search_fields = ('choice_text', 'question__question_text')
    list_select_related = ('question',)
    date_hierarchy = 'created_at'
    
    def vote_percentage(self, obj):
        """Display vote percentage with progress bar"""
        percentage = obj.vote_percentage()
        if percentage > 0:
            return format_html(
                '<div style="width:100px; background-color:#f8f9fa; border-radius:3px;">'
                '<div style="width:{}px; background-color:#007bff; height:20px; border-radius:3px; text-align:center; color:white; font-size:12px; line-height:20px;">'
                '{}%</div></div>',
                min(percentage, 100), round(percentage, 1)
            )
        return "0%"
    vote_percentage.short_description = 'Vote %'
    vote_percentage.allow_tags = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model"""
    list_display = ('name', 'slug', 'color_display', 'icon_display', 'is_active', 'question_count', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Appearance', {
            'fields': ('color', 'icon'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def color_display(self, obj):
        """Display color as a colored box"""
        return format_html(
            '<div style="width:20px; height:20px; background-color:{}; border:1px solid #ccc; border-radius:3px;"></div>',
            obj.color
        )
    color_display.short_description = 'Color'
    color_display.allow_tags = True
    
    def icon_display(self, obj):
        """Display icon if available"""
        if obj.icon:
            return format_html('<i class="{}"></i> {}', obj.icon, obj.icon)
        return '-'
    icon_display.short_description = 'Icon'
    icon_display.allow_tags = True
    
    def question_count(self, obj):
        """Display number of questions in this category"""
        return obj.question_count()
    question_count.short_description = 'Questions'


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Admin configuration for Person model"""
    list_display = ('full_name', 'email', 'phone', 'gender', 'age_display', 'is_active', 'created_at')
    list_filter = ('gender', 'is_active', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    list_editable = ('is_active',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Additional Details', {
            'fields': ('birth_date', 'gender', 'bio', 'avatar'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def age_display(self, obj):
        """Display age if birth_date is available"""
        age = obj.age
        return f'{age} years' if age else '-'
    age_display.short_description = 'Age'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Admin configuration for Article model"""
    list_display = ('title', 'author', 'category', 'status', 'views', 'like_count', 'created_at')
    list_filter = ('status', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    list_editable = ('status',)
    
    fieldsets = (
        ('Article Content', {
            'fields': ('title', 'slug', 'content', 'featured_image')
        }),
        ('Classification', {
            'fields': ('author', 'category', 'tags', 'status')
        }),
        ('Statistics', {
            'fields': ('views',),
            'classes': ('collapse',)
        }),
    )
    
    filter_horizontal = ('tags', 'likes')
    
    def like_count(self, obj):
        """Display number of likes"""
        return obj.like_count()
    like_count.short_description = 'Likes'
    
    def get_queryset(self, request):
        """Optimize queryset"""
        return super().get_queryset(request).select_related(
            'author', 'category'
        ).prefetch_related('tags', 'likes')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin configuration for Tag model"""
    list_display = ('name', 'article_count', 'created_at')
    search_fields = ('name',)
    
    def article_count(self, obj):
        """Display number of articles with this tag"""
        return obj.article_set.count()
    article_count.short_description = 'Articles'


# Admin site customization
admin.site.site_header = 'Django Polls Administration'
admin.site.site_title = 'Polls Admin'
admin.site.index_title = 'Welcome to Polls Administration'
