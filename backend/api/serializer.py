from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group

from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer

from .models import Comment


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


# class UserSerializer(HyperlinkedModelSerializer):

#     password = serializers.CharField(
#         write_only=True,
#         required=True,
#         help_text='Leave empty if no change needed',
#         style={'input_type': 'password', 'placeholder': 'Password'}
#     )

#     class Meta:
#         model = User
#         fields = [
#             'url',
#             'username',
#             'email',
#             'first_name',
#             'last_name',
#             'password',
#             # 'password2',
#             'groups'
#         ]

#     # def create(self, validated_data):
#     #     validated_data['password'] = make_password(validated_data.get('password'))
#     #     return super(UserSerializer, self).create(validated_data)

#     def create(self, validated_data):
#         user = super().create(validated_data)
#         user.set_password(validated_data['password'])
#         user.save()
#         return user

#     def update(self, instance, validated_data):
#         user = super().update(instance, validated_data)
#         try:
#             user.set_password(validated_data['password'])
#             user.save()
#         except KeyError:
#             pass
#         return user


# class GroupSerializer(HyperlinkedModelSerializer):

#     class Meta:
#         model = Group
#         fields = [
#             'url',
#             'name',
#         ]


# class UserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = '__all__'
#         fields = [
#             'url',
#             'username',
#             'email',
#             'first_name',
#             'last_name',
#             'password',
#             # 'password2',
#             'groups',
#             'permissions'
#         ]
