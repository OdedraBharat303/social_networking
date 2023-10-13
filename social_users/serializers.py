from rest_framework import serializers
from .models import CustomUser

class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(required=False, write_only=True)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class UserSearchSerializer(serializers.Serializer):
    search_keyword = serializers.CharField(max_length=100, allow_blank=False, trim_whitespace=True,)

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'name']

class FriendRequestSerializer(serializers.Serializer):
    to_user_id = serializers.IntegerField()

class ListFriendsSerializer(serializers.Serializer):
    pass
    