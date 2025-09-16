from django.contrib.auth.models import Group, User
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from tutorial.quickstart.serializers_tutorial5 import GroupSerializer, UserSerializer, PostSerializer
from tutorial.quickstart.models import Post
from tutorial.quickstart.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly


@api_view(['GET'])
def api_root(request, format=None):
    """
    API Root - Entry point with links to all available endpoints.
    """
    return Response({
        'posts': reverse('post-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
        'groups': reverse('group-list', request=request, format=format),
        'current-user': reverse('current-user', request=request, format=format),
    })


# Post Views with Hyperlinked serializers
class PostList(generics.ListCreateAPIView):
    """
    List all posts, or create a new post.
    Uses hyperlinked serializers for better API navigation.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a post instance.
    Uses hyperlinked serializers with ownership permissions.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# User Views with Hyperlinked serializers  
class UserList(generics.ListAPIView):
    """
    List all users with hyperlinked posts relationships.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetail(generics.RetrieveAPIView):
    """
    Retrieve a user instance with hyperlinked posts relationships.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# Group Views with Hyperlinked serializers
class GroupList(generics.ListCreateAPIView):
    """
    List all groups with hyperlinked relationships.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [IsAdminOrReadOnly]


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a group with hyperlinked relationships.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminOrReadOnly]


# Current user endpoint
@api_view(['GET'])
@permissions.permission_classes([permissions.IsAuthenticated])
def current_user(request, format=None):
    """
    Get information about the currently authenticated user with hyperlinked data.
    """
    serializer = UserSerializer(request.user, context={'request': request})
    return Response(serializer.data)
