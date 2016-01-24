# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.template import RequestContext
from django.template.loader import render_to_string
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.context_processors import csrf
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

## Only for debug
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# end of debug

User = get_user_model()


def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        #remember = request.POST.get('remember', '')
        user = None
        users = get_user_model().objects.filter(Q(username=username) | Q(email=username))
        for user in users:
            if user.check_password(password):
                if user.is_active:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    auth.login(request, user)
                    return redirect('/')
                elif user.has_email():
                    args['login_error'] = u'Аккаунт не активирован! Чтобы завершить активацию, тебе нужно пройти по ссылке из письма. <a href="/auth/request_email/">Запросить письмо</a> еще раз...'
                else:
                    args['login_error'] = u'Регистрация была из игры. Укажи там свой email!'
            else:
                args['login_error'] = 'Пользователь не найден, или пароль не верен!'
        return render_to_response("login.html",
                                  args,
                                  context_instance=RequestContext(request))
    else:
        return render_to_response("login.html",
                                  context_instance=RequestContext(request))


def logout(request):
    auth.logout(request)
    return redirect('/')


def validate_email_unique(value):
    exists = User.objects.filter(email=value)
    if exists:
        raise ValidationError("Email address %s already exits, must be unique" % value)


class RegisterForm(UserCreationForm):
    username = forms.CharField(label=_("Ваш Ник"), max_length=30, required=True,
                               error_messages={'required': 'Пожалуйста, введи свой Ник (как в игре).'})
    password1 = forms.CharField(label=_("Пароль"), widget=forms.PasswordInput, max_length=30, required=True)
    password2 = forms.CharField(label=_("Повтори пароль"), widget=forms.PasswordInput, max_length=30, required=True)
    email = forms.EmailField(label=_("Email"), required=True, validators=[validate_email_unique])

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2", )

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user.email = self.cleaned_data.get("email")
        if commit:
            user.save()
        return user


def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = RegisterForm()
    if request.POST:
        newuser_form = RegisterForm(request.POST)
        if newuser_form.is_valid():
            # Save new user into DB
            newuser_form.save()
            # Authenticate user right here
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                        password=newuser_form.cleaned_data['password2'])
            return redirect('/')
        else:
            args['form'] = newuser_form
    return render_to_response("register.html",
                              args,
                              context_instance=RequestContext(request))

