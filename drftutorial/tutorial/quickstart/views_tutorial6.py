from django.contrib.auth.models import Group, User
from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view
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
    })


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet that automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for posts.
    
    Additionally provides a `by_user` action to get posts by specific user.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """Automatically set the owner to the current user."""
        serializer.save(owner=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_posts(self, request):
        """Custom action to get current user's posts."""
        posts = Post.objects.filter(owner=request.user)
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def set_favorite(self, request, pk=None):
        """Custom action to mark a post as favorite (demo only)."""
        post = self.get_object()
        # This is just a demo - in real app you'd have a favorite model/field
        return Response({'status': f'Post "{post.title}" marked as favorite by {request.user.username}'})


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet that automatically provides `list` and `retrieve` actions for users.
    Read-only because users shouldn't be created/modified via API.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        """Custom action to get all posts by a specific user."""
        user = self.get_object()
        posts = Post.objects.filter(owner=user)
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = PostSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet that automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for groups.
    
    Only admins can create/modify groups.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def members(self, request, pk=None):
        """Custom action to get all members of a group."""
        group = self.get_object()
        users = group.user_set.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)
