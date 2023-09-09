from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm, LoginForm


class BaseSignupForm(SignupForm):

    def save(self, request):
        user = super(BaseSignupForm, self).save(request)
        base_group = Group.objects.get(name='common')
        base_group.user_set.add(user)

        return user
