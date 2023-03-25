# from django.contrib.auth.models import User. Group
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Comment

from django.contrib.auth import get_user_model as user_model


User = user_model()


class CommentSerializer(ModelSerializer):
    """
    Serializer for Comment model
    """
    class Meta:
        model = Comment
        fields = '__all__'


# class UserSerializer(serializers.ModelSerializer):
#     """
#     Serializer for User model
#     """
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email')


# class RegisterSerializer(serializers.ModelSerializer):
#     """
#     Serializer for User model for registration
#     """
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'password')
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             validated_data['username'], validated_data['email'], validated_data['password'])

#         return user


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    overview = serializers.CharField()
    release_date = serializers.DateField()
    vote_average = serializers.FloatField()
    poster_path = serializers.CharField()
    popularity = serializers.FloatField()
    adult = serializers.BooleanField()
    # imdb_id = serializers.CharField()
    genre_ids = serializers.ListField()


class GenreSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
