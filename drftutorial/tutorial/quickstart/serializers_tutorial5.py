from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """
    Hyperlinked serializer for Post model with owner relationship.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Post
        fields = ['url', 'id', 'title', 'content', 'owner', 'created', 'updated']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Hyperlinked serializer for User model with posts relationship.
    """
    posts = serializers.HyperlinkedRelatedField(
        many=True, 
        view_name='post-detail', 
        read_only=True
    )
    
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'groups', 'posts']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """
    Hyperlinked serializer for Group model.
    """
    class Meta:
        model = Group
        fields = ['url', 'id', 'name']
