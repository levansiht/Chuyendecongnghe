from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
import datetime

# Create your models here.

# Custom Manager for Question
class QuestionManager(models.Manager):
    def published_recently(self):
        return self.filter(pub_date__gte=timezone.now() - datetime.timedelta(days=7))
    
    def search(self, query):
        return self.filter(
            Q(question_text__icontains=query) | 
            Q(choices__choice_text__icontains=query)
        ).distinct()


class Question(models.Model):
    question_text = models.CharField(max_length=200, help_text="Enter your question here")
    pub_date = models.DateTimeField('date published', default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Custom manager
    objects = QuestionManager()
    
    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    def get_absolute_url(self):
        return reverse('polls:detail', kwargs={'pk': self.pk})
    
    def total_votes(self):
        return sum(choice.votes for choice in self.choices.all())
    
    class Meta:
        ordering = ['-pub_date']
        verbose_name = "Poll Question"
        verbose_name_plural = "Poll Questions"
        indexes = [
            models.Index(fields=['pub_date']),
            models.Index(fields=['author', 'pub_date']),
        ]


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.choice_text
    
    def vote_percentage(self):
        total_votes = self.question.total_votes()
        if total_votes == 0:
            return 0
        return (self.votes / total_votes) * 100
    
    class Meta:
        ordering = ['-votes']
        unique_together = ['question', 'choice_text']


class Person(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        if self.birth_date:
            today = datetime.date.today()
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return None
    
    def get_absolute_url(self):
        return reverse('person-detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = "Person"
        verbose_name_plural = "People"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True, help_text="URL-friendly version of the name")
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#007bff", help_text="Hex color code")
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'slug': self.slug})
    
    def question_count(self):
        return self.question_set.filter(is_active=True).count()
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"


# Advanced Model with Many-to-Many relationship
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    featured_image = models.URLField(blank=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, blank=True, related_name='liked_articles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'slug': self.slug})
    
    def like_count(self):
        return self.likes.count()
    
    def is_published(self):
        return self.status == 'published'
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['author', 'created_at']),
        ]
    
    class Meta:
        verbose_name_plural = "categories"


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
