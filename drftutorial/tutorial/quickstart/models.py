from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    A simple blog post model to demonstrate authentication and permissions.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    owner = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title
