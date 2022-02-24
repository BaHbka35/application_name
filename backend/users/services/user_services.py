from users.models import User, UserBalance


class UserService:
    """Class witch contain all logic belongs to user"""

    @staticmethod
    def create_user_and_his_balance(data: dict) -> User:
        """Creates user and create his balance."""
        user = User.objects.create_user(**data)
        UserBalance(user=user).save()
        return user

    @staticmethod
    def activate_user(user: User) -> User:
        """Activates user account."""
        user.is_activated = True
        user.save()
        return user

    @staticmethod
    def change_user_password(user: User, password: str) -> User:
        """Changes user password."""
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def update_user_data(user: User, data: dict) -> User:
        """Update user data."""
        user.first_name = data['first_name']
        user.surname = data['surname']
        user.username = data['username']
        user.slug = user.username
        user.age = data['age']
        user.gender = data['gender']
        user.training_experience = data['training_experience']
        user.trains_now = data['trains_now']
        user.save()
        return user

    @staticmethod
    def has_user_enough_coins(user: User, required_coins_amount: int) -> bool:
        """Has user more or equal coins amount than was given"""
        return user.balance.coins_amount >= required_coins_amount

    @staticmethod
    def add_coins_for_user(user: User, coins_amount: int) -> None:
        """Add coins to user balance"""
        user.balance.coins_amount += coins_amount
        user.balance.save()

    @staticmethod
    def withdraw_coins_from_user(user: User, coins_amount: int) -> None:
        """withdraw coins from user balance."""
        user.balance.coins_amount -= coins_amount
        user.balance.save()
