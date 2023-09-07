from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from .models import BaseRegisterForm


class BaseRegisterView(CreateView):

    model = User
    form_class = BaseRegisterForm
    success_url = 'sign/'


class CompleteSignupView(TemplateView):

    template_name = 'sign/complete_signup.html'
