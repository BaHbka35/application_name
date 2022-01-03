import hashlib

from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string


def get_activation_token(user):
    s = f"{user.id}{user.username}"
    s = s.encode()
    hash_object = hashlib.md5(s + settings.SECRET_KEY_BYTES)
    return hash_object.hexdigest()


def send_email_for_activate_account(request, user):
    subject = 'Account activation'
    token = get_activation_token(user)
    current_site = get_current_site(request)
    content = {
        'user': user,
        'id': user.id,
        'token': token,
        'domain': current_site.domain
    }
    html_message = render_to_string('users/email_for_activation_account.html', content)
    to_email = user.email
    email = EmailMessage(subject, html_message, to=[to_email])
    email.send()

