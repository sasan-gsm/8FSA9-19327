from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
        read_only_fields = ["id"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token serializer login with username or email."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"] = serializers.EmailField(required=False)

        if "username" in self.fields:
            self.fields["username"].required = False

    def validate(self, attrs):
        username = attrs.get("username")
        email = attrs.get("email")

        if not username and not email:
            raise serializers.ValidationError(
                {"error": "Username or email must be provided"}
            )

        if email and not username:
            try:
                user = User.objects.get(email=email)
                attrs["username"] = user.username
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    {"email": "No user found with this email address"}
                )
        return super().validate(attrs)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name

        return token
