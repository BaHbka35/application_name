from django.contrib.sites.shortcuts import get_current_site


def get_current_site_domain(request: 'django_request') -> str:
    """Returns domain."""
    return get_current_site(request).domain


def get_amended_data_for_response_from_signup_view(data: dict) -> dict:
    """Removes not needed field from data for response"""
    del data['password']
    data['message'] = 'Check your email for activate account.'
    return data
