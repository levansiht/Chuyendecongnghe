from django.contrib.auth.models import Group, User
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from tutorial.quickstart.serializers import GroupSerializer, UserSerializer, PostSerializer
from tutorial.quickstart.models import Post
from tutorial.quickstart.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly, IsOwnerOrAdmin


# Post Views with Authentication & Permissions
class PostList(generics.ListCreateAPIView):
    """
    List all posts, or create a new post.
    Only authenticated users can create posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set the owner to the current user
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a post instance.
    Only the owner can update/delete their posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# Enhanced User Views with Posts relationship
class UserList(generics.ListAPIView):
    """
    List all users (read-only).
    Shows the posts created by each user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetail(generics.RetrieveAPIView):
    """
    Retrieve a user instance (read-only).
    Shows the posts created by the user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# Group Views with Admin permissions
class GroupList(generics.ListCreateAPIView):
    """
    List all groups, create new groups.
    Only admins can create groups.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [IsAdminOrReadOnly]


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a group.
    Only admins can modify groups.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminOrReadOnly]


# Demo view showing current user info
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    """
    Get information about the currently authenticated user.
    """
    user = request.user
    serializer = UserSerializer(user, context={'request': request})
    return Response(serializer.data)
