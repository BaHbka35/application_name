from django.test import TestCase

from users.models import User


def testing_basic_fields(self, user: User, name: str) -> None:
    """Validates the fields of the created user."""
    self.assertEqual(user.first_name, f'{name}_first_name')
    self.assertEqual(user.surname, f'{name}_surname')
    self.assertEqual(user.username, f'{name}')
    self.assertEqual(user.slug, f'{name}')
    self.assertEqual(user.email, f'{name}@gmail.com')


def checks_superuser_and_stuff_status(self, user, value: bool) -> None:
    """Validates the admins fields of the created user."""
    self.assertEqual(user.is_superuser, value)
    self.assertEqual(user.is_staff, value)


def testing_extra_fields_with_default_value(self, user: User) -> None:
    """Tests that extra fields have default values."""
    self.assertEqual(user.age, None)
    self.assertEqual(user.gender, None)
    self.assertEqual(user.training_experience, None)
    self.assertEqual(user.trains_now, None)
    self.assertEqual(user.training_experience, None)
    self.assertEqual(user.is_active, True)


class CreatingUserManagerTests(TestCase):
    """
    Class for testing correct working 'objects' manager
    for creating base user.
    """

    def test_creating_base_user_with_basic_fields(self):
        """Tests correct creating base user with basic fields."""
        user = User.objects._create_base_user(
            first_name='test_first_name',
            surname='test_surname',
            username='test',
            email='test@gmail.com',
            password='password',
        )
        testing_basic_fields(self, user, 'test')
        testing_extra_fields_with_default_value(self, user)

    def test_creating_base_user_without_first_name(self):
        """Tests creating user without first name."""
        with self.assertRaises(ValueError):
            User.objects._create_base_user(
                first_name='',
                surname='test_surname',
                username='test',
                email='test@gmail.com',
                password='password',
            )

    def test_creating_base_user_without_surname(self):
        """Tests creating user without surname."""
        with self.assertRaises(ValueError):
            User.objects._create_base_user(
                first_name='test_first_name',
                surname='',
                username='test',
                email='test@gmail.com',
                password='password',
            )

    def test_creating_base_user_without_username(self):
        """Tests creating user without username."""
        with self.assertRaises(ValueError):
            User.objects._create_base_user(
                first_name='test_first_name',
                surname='test_surname',
                username='',
                email='test@gmail.com',
                password='password',
            )

    def test_creating_base_user_without_email(self):
        """Tests creating user without email."""
        with self.assertRaises(ValueError):
            User.objects._create_base_user(
                first_name='test_first_name',
                surname='test_surname',
                username='test',
                email='',
                password='password',
            )

    def test_creating_base_user_without_password(self):
        """Tests creating user without password."""
        with self.assertRaises(ValueError):
            User.objects._create_base_user(
                first_name='test_first_name',
                surname='test_surname',
                username='test',
                email='test@gmail.com',
                password='',
            )

    def test_creating_base_user_with_not_existing_fields(self):
        """Tests creating user with not existing fields."""
        with self.assertRaises(TypeError):
            User.objects._create_base_user(
                first_name='test_first_name',
                surname='test_surname',
                username='test',
                email='test@gmail.com',
                password='password',
                some_field='some_field',
            )

    def test_creating_base_user_with_all_fields_with_one_type_values(self):
        """Tests creating user with all fields."""
        user = User.objects._create_base_user(
            first_name='test_first_name',
            surname='test_surname',
            username='test',
            email='test@gmail.com',
            password='password',
            age=18,
            gender='male',
            training_experience=5,
            trains_now=True,
            )
        self.assertEqual(user.age, 18)
        self.assertEqual(user.gender, 'male')
        self.assertEqual(user.training_experience, 5)
        self.assertEqual(user.trains_now, True)

    def test_creating_base_user_with_all_fields_with_one_type_values(self):
        """Tests creating user with all field but that have different value."""
        user = User.objects._create_base_user(
            first_name='test_first_name',
            surname='test_surname',
            username='test',
            email='test@gmail.com',
            password='password',
            gender='female',
            training_experience=5.5,
            trains_now=False,
            )
        self.assertEqual(user.gender, 'female')
        self.assertEqual(user.training_experience, 5.5)
        self.assertEqual(user.trains_now, False)


class CreatingSuperuserTests(TestCase):
    """Class for testing function which gives base user status superuser"""

    def test_creating_superuser_without_admin_status(self):
        """
        Tests correct creating superuser with basic fields
        and without admin status. User must be with admin status.
        """
        user = User.objects.create_superuser(
            first_name='test_first_name',
            surname='test_surname',
            username='test',
            email='test@gmail.com',
            password='password',
            is_staff=False,
            is_superuser=False,
            is_activated=False,
        )
        testing_basic_fields(self, user, 'test')
        checks_superuser_and_stuff_status(self, user, True)


class CreatingRegularUserTests(TestCase):
    """Class for testing function which gives base user status regular user."""

    def test_creating_regular_user_with_admin_status(self):
        """
        Tests correct creating regular user with basic fields
        and admin status. User must be without admin status.
        """
        user = User.objects.create_user(
            first_name='test_first_name',
            surname='test_surname',
            username='test',
            email='test@gmail.com',
            password='password',
            is_staff=True,
            is_superuser=True,
            is_activated=True,
            )
        testing_basic_fields(self, user, 'test')
        checks_superuser_and_stuff_status(self, user, False)
