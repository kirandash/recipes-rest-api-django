# get User Model from default Django auth
# authenticate: django helper command for django auth system
from django.contrib.auth import get_user_model, authenticate
# for translatable messages that we will o/p to terminal
from django.utils.translation import ugettext_lazy as _

# serializers from rest_framework
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User object"""

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

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        # remove password. None is the default value to be passed with pop
        password = validated_data.pop('password', None)
        # extending from super(), to include default ones + overwrite
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    # by default django trims whitespace, we will allow it for pwd field
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            # using rest_framework built in error handler
            raise serializers.ValidationError(msg, code='authentication')

        # after validation is successful overwrite the user attr and return
        attrs['user'] = user
        return attrs
