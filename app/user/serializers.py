# get User Model from default Django auth
from django.contrib.auth import get_user_model

# serializers from rest_framework
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializers for the User object"""

    class Meta:
        # get user model
        model = get_user_model()
        # fields to map from JSON to model
        fields = ('email', 'password', 'name')
        # set extra args for pwd: write only password, min length validation
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)
