from django.contrib.auth.models import Group, User
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from tutorial.quickstart.serializers import GroupSerializer, UserSerializer


class UserList(APIView):
    """
    List all users, or create a new user.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        users = User.objects.all().order_by('-date_joined')
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupList(APIView):
    """
    List all groups, or create a new group.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        groups = Group.objects.all().order_by('name')
        serializer = GroupSerializer(groups, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GroupSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupDetail(APIView):
    """
    Retrieve, update or delete a group instance.
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        group = self.get_object(pk)
        serializer = GroupSerializer(group, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        group = self.get_object(pk)
        serializer = GroupSerializer(group, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        group = self.get_object(pk)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
