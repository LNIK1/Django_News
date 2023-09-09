from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm, LoginForm
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:

        model = Post
        fields = [
            'author',
            'title',
            'categories',
            'text',
        ]
        widgets = {
            'title': forms.Textarea(attrs={'class': 'form-text', 'cols': 70, 'rows': 3}),
            'text': forms.Textarea(attrs={'class': 'form-text', 'cols': 70, 'rows': 10}),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")
        author = cleaned_data.get("author")

        if title is None or title == "":
            raise ValidationError({
                "title": "Заголовок не должен быть пустым"
            })

        if text is None or text == "":
            raise ValidationError({
                "text": "Содержание должно быть заполнено"
            })

        if author is None:
            raise ValidationError({
                "author": "Необходимо указать автора"
            })

        return cleaned_data


class BaseSignupForm(SignupForm):

    def save(self, request):
        user = super(BaseSignupForm, self).save(request)
        base_group = Group.objects.get(name='base')
        base_group.user_set.add(user)

        return user
