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
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from .views import CommentApiView
# from .views import list_user_view, update_user_view, delete_user_view
# from .views import UserViewSet
from .views import CommentDetailAPIView
from .views import CommentFromContentAPIView
# , GroupViewSet


# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'group', GroupViewSet)

urlpatterns = [

    path('comments/', CommentApiView.as_view()),
    path('comments/<int:content_id>/', CommentFromContentAPIView.as_view()),
    path('comment/<int:comment_id>/', CommentDetailAPIView.as_view()),
    # path('', include(router.urls)),

    #  path("user/", list_user_view),
    # path("user/<int:pk>/", list_user_view),

    # path("create_user/", CreateUserAPIView.as_view(), name="user_create"),

    # path("update_user/<int:pk>/", update_user_view),
    # path("update_user/<int:pk>", update_user_view),

    # path("delete_user/<int:pk>/", delete_user_view),
    # path("delete_user/<int:pk>", delete_user_view),

]
