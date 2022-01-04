import hashlib

from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string


def get_activation_token(user):
    """
    Create token which will be send on user email
    for activate user account.
    """
    forming_str = f"{user.id}{user.username}"
    forming_str = forming_str.encode()
    hash_object = hashlib.md5(forming_str + settings.SECRET_KEY_BYTES)
    return hash_object.hexdigest()


def __get_content_for_email(request, user):
    """
    Forms conten for latter which will be
    sent to user email fro activate account
    """
    token = get_activation_token(user)
    current_site = get_current_site(request)
    content = {
        'user': user,
        'id': user.id,
        'token': token,
        'domain': current_site.domain
    }
    return content


def __get_ready_email(content, user):
    """Create email wich is ready to be sent to user."""
    subject = 'Account activation'
    html_message = render_to_string('users/email_for_activation_account.html', content)
    user_email = user.email
    email = EmailMessage(subject, html_message, to=[user_email])
    return email


def send_email_for_activate_account(request, user):
    """Send email to user email with activation link."""
    content = __get_content_for_email(request, user)
    ready_email = __get_ready_email(content, user)
    ready_email.send()

