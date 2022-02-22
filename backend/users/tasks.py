from config.celery import app

from .models import User
from .services.email_services import EmailService


@app.task
def send_email_for_activate_account(current_site_domain: str, user_id: int) -> None:
    """"""
    user = User.objects.get(id=user_id)
    EmailService.send_email_for_activate_account(current_site_domain, user)


@app.task
def send_email_for_confirm_changing_email(current_site_domain: str, user_id: int,
                                          new_user_email: str) -> None:
    """"""
    user = User.objects.get(id=user_id)
    EmailService.send_email_for_confirm_changing_email(current_site_domain,
                                                       user, new_user_email)
