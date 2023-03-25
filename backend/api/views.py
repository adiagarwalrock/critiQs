import io

from django.contrib.auth.models import User, Group
# from django.contrib.auth import login
# from django.db.models import F
# from django.http.response import JsonResponse
# from django.shortcuts import render
# from django.views.decorators.http import require_POST

from rest_framework import (
    permissions,
    status
)
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
    ListCreateAPIView,
)
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework.decorators import api_view
# from rest_framework.parsers import JSONParser
# from rest_framework.viewsets import ModelViewSet

from .models import Comment
from .serializer import (
    CommentSerializer,
    UserSerializer,
    RegisterSerializer
)


MOVIE_API_KEY = 'f6792b478e6716a30e6af1fb17c30419'


class MovieAPIView(APIView):

    def get(self, request, *args, **kwargs):
        '''
        API method for getting movies
        '''


class CommentListCreateAPIView(ListCreateAPIView):
    """
    List all comments & Create a new comment
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetailDataView(RetrieveAPIView):
    """
    Retrieve a comment details
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDeleteAPIView(DestroyAPIView):
    """
    Delete a comment after checking if the
    request user is the owner of the comment
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        if instance.user == self.request.user:
            self.perform_destroy(instance)
            return Response(
                {"response": "Comment deleted!"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"response": "You are not the owner of this comment!"},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserCommentListAPIView(ListAPIView):
    """
    List all comments of a user
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(user=user)


class CommentUpdateAPIView(UpdateAPIView):
    """
    API to update a comment by the owner of the comment
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, *args, **kwargs):
        instance = self.get_object()
        if instance.user == self.request.user:
            self.perform_update(instance)
            return Response(
                {"response": "Comment updated!"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"response": "You are not the owner of this comment!"},
            status=status.HTTP_400_BAD_REQUEST
        )


class ContentCommentsAPIView(APIView):
    """
    API to get comments for a given content
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, content_id, *args, **kwargs):
        '''
        API to FETCH comments for a given content id.

        args:
            content_id: id of the content
            type: int

        returns:
            list: comments for a given content id
            type: list of dict
        '''
        comment_instance = Comment.objects.filter(
            content_id=content_id).order_by('-date_created')
        if not comment_instance:
            return Response(
                {"detail": "Object with given id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CommentSerializer(comment_instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class CommentApiView(APIView):

#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         '''
#         API to list all the comments
#         '''
#         comments = Comment.objects.all().order_by('-date_created')
#         serializer = CommentSerializer(comments, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request, *args, **kwargs):
#         '''
#         API to create a new comment
#         '''
#         fields = {'content_id', 'body', 'user'}

#         if request.data.keys() < fields:
#             return Response(
#                 {"response": "Please provide all the required fields"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         if not User.objects.filter(id=int(*request.data.get('user'))).exists():
#             return Response(
#                 {"response": "User does not exist. Please provide a valid user id"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         data = {
#             'content_id': request.data.get('content_id'),
#             'user': request.data.get('user'),
#             'body': request.data.get('body')
#         }
#         serializer = CommentSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CommentDetailAPIView(APIView):
#     """
#     API Class to Read, Update and Delete a comment
#     """

#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self, comment_id):
#         try:
#             return Comment.objects.get(id=int(comment_id))
#         except Comment.DoesNotExist:
#             return None

#     def get(self, request, comment_id, *args, **kwargs):
#         '''
#         API for fetching perticular comment using "comment_id".
#         args:
#             comment_id: id of the comment
#             type: int
#         '''
#         comment_instance = self.get_object(comment_id)
#         if not comment_instance:
#             return Response(
#                 {"response": "Object with given id does not exist"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         serializer = CommentSerializer(comment_instance)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, comment_id, *args, **kwargs):
#         '''
#         API method to update a comment
#         '''
#         comment_instance = self.get_object(comment_id)
#         if not comment_instance:
#             return Response(
#                 {"response": "Object with the given id does not exist"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         data = {
#             'content_id': request.data.get('content_id'),
#             'user': request.user.id,
#             'body': request.data.get('body'),
#         }
#         serializer = CommentSerializer(
#             instance=comment_instance,
#             data=data,
#             partial=True,
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, comment_id, *args, **kwargs):
#         '''
#         API to delete a comment
#         '''
#         comment_instance = self.get_object(comment_id)
#         if not comment_instance:
#             return Response(
#                 {"res": "Object with comment id does not exists"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         comment_instance.delete()
#         return Response(
#             {"response": "Object deleted!"},
#             status=status.HTTP_200_OK
#         )
