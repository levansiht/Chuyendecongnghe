from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'owner', 'created', 'updated']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'groups', 'posts']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
