from datetime import datetime
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):

    d = context['request'].GET.copy()

    for k, v in kwargs.items():
        d[k] = v

    return d.urlencode()


@register.simple_tag()
def cur_time(format_str='%b %d %Y'):

    return datetime.utcnow().strftime(format_str)


# Middleware для определения мобильное устройство или ПК
# class MobileOrFullMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         response = self.get_response(request)
#         if request.mobile:
#             prefix = "mobile/"
#         else:
#             prefix = "full/"
#         response.template_name = prefix + response.template_name
#         return response
