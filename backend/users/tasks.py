from config.celery import app

from .models import User
from .services.email_services import EmailSendingService


@app.task
def send_email_for_activate_account(current_site_domain: str, user_id: int) -> None:
    """Sends email to user for account activation."""
    user = User.objects.get(id=user_id)
    EmailSendingService.send_email_for_activate_account(current_site_domain,
                                                        user)


@app.task
def send_email_for_confirm_changing_email(current_site_domain: str, user_id: int,
                                          new_user_email: str) -> None:
    """
    Sends email to new user email address
    for confirm changing email address.
    """
    user = User.objects.get(id=user_id)
    EmailSendingService.send_email_for_confirm_changing_email(
        current_site_domain, user, new_user_email)
