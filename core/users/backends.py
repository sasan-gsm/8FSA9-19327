import re
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from typing import Optional, Any

User = get_user_model()


class CustomAuthenticationBackend(ModelBackend):
    """
    Authentication backend that allows authentication with either username or email.
    """

    def authenticate(
        self,
        request: Any,
        username: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs: Any,
    ) -> Optional[User]:
        if username is None or password is None:
            return None

        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", username):
            lookup_field = "email"
        else:
            lookup_field = "username"

        try:
            lookup_kwargs = {lookup_field: username}
            user = User.objects.get(**lookup_kwargs)

            if user.check_password(password):
                return user

        except User.DoesNotExist:
            User().set_password(password)

        return None
