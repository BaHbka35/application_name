from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Custom user manager."""

    def _create_base_user(self, first_name, surname, username,
                          email, password, **extra_fields):

        if not first_name:
            raise ValueError("User must have first name")
        if not surname:
            raise ValueError("User must have surname name")
        if not username:
            raise ValueError("User must have username name")
        if not email:
            raise ValueError("User must have email")
        if not password:
            raise ValueError("User must have password name")

        email = self.normalize_email(email)
        try:
            user = self.model(first_name=first_name,
                              surname=surname,
                              username=username,
                              email=email,
                              password=None,
                              **extra_fields)
        except TypeError:
            raise TypeError("Unexisting field of model")

        user.set_password(password)
        user.slug = username
        user.save()
        return user
        

    def create_user(self, first_name, surname, username,
                    email, password, **extra_fields):

        extra_fields["is_superuser"] = False
        extra_fields["is_staff"] = False
        extra_fields["is_activated"] = False
        return self._create_base_user(first_name, surname, username,
                                      email, password, **extra_fields)

    def create_superuser(self, first_name, surname, username,
                         email, password, **extra_fields):

        extra_fields["is_superuser"] = True
        extra_fields["is_staff"] = True
        extra_fields["is_activated"] = True
        return self._create_base_user(first_name, surname, username,
                                      email, password, **extra_fields)
