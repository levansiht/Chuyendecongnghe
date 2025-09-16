from django.contrib.auth.models import Group, User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from tutorial.quickstart.serializers import GroupSerializer, UserSerializer


class UserList(generics.ListCreateAPIView):
    """
    List all users, or create a new user using generic views.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a user instance using generic views.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class GroupList(generics.ListCreateAPIView):
    """
    List all groups, or create a new group using generic views.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a group instance using generic views.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
