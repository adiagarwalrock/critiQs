import io

from django.contrib.auth.models import User, Group
from django.db.models import F
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from rest_framework import status, generics
from rest_framework import permissions
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication
)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# from .serializer import UserSerializer
# from .serializer import GroupSerializer
from .models import Comment
from .serializer import CommentSerializer
# from .serializer import CommentHyperlinkedSerializer


class CommentApiView(APIView):
    authentication_classes = [
        BasicAuthentication,
        SessionAuthentication,
        TokenAuthentication
    ]
    permission_class = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        API to list all the comments
        '''
        comments = Comment.objects.all().order_by('-date_created')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        API to create a new comment
        '''
        data = {
            'content_id': request.data.get('content_id'),
            'user': request.user.id,
            'body': request.data.get('body'),
        }
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentFromContentAPIView(APIView):
    authentication_classes = [
        BasicAuthentication,
        SessionAuthentication,
        TokenAuthentication
    ]
    permission_class = [permissions.IsAuthenticated]

    def get(self, request, content_id, *args, **kwargs):
        '''
        API to get comments for a given content
        '''
        comment_instance = Comment.objects.filter(
            content_id=content_id).order_by('-date_created')
        if not comment_instance:
            return Response(
                {"response": "Object with given id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CommentSerializer(comment_instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentDetailAPIView(APIView):
    authentication_classes = [
        BasicAuthentication,
        SessionAuthentication,
        TokenAuthentication
    ]
    permission_class = [permissions.IsAuthenticated]

    def get_object(self, comment_id):
        try:
            return Comment.objects.get(id=int(comment_id))
        except Comment.DoesNotExist:
            return None

    def get(self, request, comment_id, *args, **kwargs):
        '''
        API for fetching comment insyance from comment id
        '''
        comment_instance = self.get_object(comment_id)
        if not comment_instance:
            return Response(
                {"response": "Object with given id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CommentSerializer(comment_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, comment_id, *args, **kwargs):
        '''
        API method to update a comment
        '''
        comment_instance = self.get_object(comment_id)
        if not comment_instance:
            return Response(
                {"response": "object with the given id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = {
            'content_id': request.data.get('content_id'),
            'user': request.user.id,
            'body': request.data.get('body'),
        }
        serializer = CommentSerializer(
            instance=comment_instance,
            data=data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id, *args, **kwargs):
        '''
        API to delete a comment
        '''
        comment_instance = self.get_object(comment_id)
        if not comment_instance:
            return Response(
                {"res": "Object with comment id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        comment_instance.delete()
        return Response(
            {"response": "Object deleted!"},
            status=status.HTTP_200_OK
        )

        # class UserViewSet(ModelViewSet):
        #     queryset = User.objects.all().order_by('-date_joined')
        #     serializer_class = UserSerializer
        #     permission_class = [permissions.IsAuthenticated]

        # class GroupViewSet(ModelViewSet):
        #     queryset = Group.objects.all()
        #     serializer_class = GroupSerializer
        #     permission_class = [permissions.IsAuthenticated]

        # @api_view(['GET'])
        # def list_user_view(request, pk=None):
        #     if request.method == 'GET':
        #         if pk is not None:
        #             try:
        #                 user = User.objects.get(pk=pk)
        #                 user_serializer = UserSerializer(user)
        #                 return JsonResponse(user_serializer.data, status=status.HTTP_302_FOUND)
        #             except User.DoesNotExist:
        #                 return JsonResponse({'message': 'The User does not exist', 'request_type': 'GET', 'function': 'list_user_api_view'}, status=status.HTTP_404_NOT_FOUND)
        #         else:
        #             user_obj = User.objects.all()
        #             user_serializer = UserSerializer(user_obj, many=True)
        #             return JsonResponse(user_serializer.data, safe=False, status=status.HTTP_302_FOUND)

        # @api_view(['PUT'])
        # def update_user_view(request, pk):
        #     # Updates any user field by referencing the user-id
        #     if request.method == 'PUT':
        #         user = User.objects.get(pk=pk)
        #         user_data = JSONParser().parse(request)

        #         user_serializer = UserSerializer(user, partial=True, data=user_data)

        #         if user_serializer.is_valid():
        #             user_serializer.save()
        #             return JsonResponse({'message': 'User was updated successfully!'}, status=status.HTTP_200_OK)
        #         return JsonResponse({'message': 'User could not be updated successfully!', 'request_type': 'PUT', 'function': 'update_user_view'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # class CreateUserAPIView(generics.CreateAPIView):
        #     queryset = User.objects.all()
        #     serializer_class = UserSerializer
        #     # fields = ['username']

        # @api_view(['DELETE'])
        # def delete_user_view(request, pk):
        #     if request.method == 'DELETE':
        #         try:
        #             user = User.objects.get(pk=pk)
        #             user.delete()
        #             return JsonResponse({'message': 'User deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        #         except User.DoesNotExist:
        #             return JsonResponse({'message': 'User does not exist', 'request_type': 'DELETE', 'function': 'delete_user_view'}, status=status.HTTP_404_NOT_FOUND)
