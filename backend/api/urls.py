"""critiQs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from rest_framework.authtoken import view s
from django.contrib import admin
from django.urls import path, include

from .views import (
    #     CommentApiView,
    #     CommentDetailAPIView,

    CommentListCreateAPIView,
    UserCommentListAPIView,
    CommentDetailDataView,
    ContentCommentsAPIView,
    CommentDeleteAPIView,
    CommentUpdateAPIView,

)

urlpatterns = [

    # List all comments & Create a new comment
    path('comment/', CommentListCreateAPIView.as_view()),

    # List all comments of a user
    path('comment/user/', UserCommentListAPIView.as_view()),

    # Retrieve a comment details
    path('comment/<int:pk>/', CommentDetailDataView.as_view()),

    # Get comments for a given content_id
    path('comment/content/<int:content_id>/',
         ContentCommentsAPIView.as_view()),

    # Delete a comment
    path('comment/<int:pk>/delete/', CommentDeleteAPIView.as_view()),

    # Update a comment
    path('comment/<int:pk>/update/', CommentUpdateAPIView.as_view()),
]
