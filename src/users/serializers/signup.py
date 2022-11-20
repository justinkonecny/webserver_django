import re

from django.contrib.auth.models import User
from rest_framework import serializers


class SignupRequestSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def create(self, validated_data) -> User:
        return User.objects.create_user(
            email=validated_data.get('email').strip().lower(),
            username=validated_data.get('username').strip().lower(),
            first_name=validated_data.get('first_name').strip(),
            last_name=validated_data.get('last_name').strip(),
            password=validated_data.get('password'),
        )

    def update(self, user: User, validated_data) -> User:
        # don't update any user object from this
        raise ValueError('cannot update user')

    @staticmethod
    def validate_email(value: str) -> str:
        if not re.compile(r'^\w+@\w+\.\w+$').match(value):
            raise serializers.ValidationError("invalid email address")
        return value

    @staticmethod
    def validate_username(value: str) -> str:
        if not re.compile(r'^\w{4,20}$').match(value):
            raise serializers.ValidationError("username must be 4 to 20 characters")
        return value

    @staticmethod
    def validate_first_name(value: str) -> str:
        if not re.compile(r'^\w{1,20}$').match(value):
            raise serializers.ValidationError("first name must be 1 to 20 letters")
        return value

    @staticmethod
    def validate_last_name(value: str) -> str:
        if not re.compile(r'^\w{1,20}$').match(value):
            raise serializers.ValidationError("last name must be 1 to 20 letters")
        return value

    @staticmethod
    def validate_password(value: str) -> str:
        if len(value) < 8:
            raise serializers.ValidationError("password must be at least 8 characters")
        return value
