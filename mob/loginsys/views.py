# -*- encoding: utf-8 -*-
import random
import hashlib
import datetime
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import auth
from django.template import RequestContext
from django.template.loader import render_to_string
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.context_processors import csrf
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

## Only for debug
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# end of debug

User = get_user_model()

# time before activate link is expired
TTE = 2


def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # remember = request.POST.get('remember', '')
        user = None
        users = get_user_model().objects.filter(Q(username=username) | Q(email=username))
        for user in users:
            if user.check_password(password):
                if user.is_active:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    auth.login(request, user)
                    return redirect('/')
                elif user.has_email():
                    args['login_error'] = u'Аккаунт не активирован! Чтобы завершить активацию, тебе нужно пройти по ссылке из письма. <a href="/auth/request/">Запросить письмо</a> еще раз...'
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
        fields = ("email", "username", "password1", "password2",)

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
            username = newuser_form.cleaned_data['username']
            reactivation(request=request, username=username)

        else:
            args['form'] = newuser_form
    return render_to_response("register.html",
                              args,
                              context_instance=RequestContext(request))

def reactivation(request, username):
    args = {}
    # Get user by username and update his profile with activation data
    user = User.objects.get(username=username)

    # Send email with activation key
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    activation_key = hashlib.sha1(salt + user.get_email()).hexdigest()
    key_expires = datetime.datetime.today() + datetime.timedelta(TTE)

    # Send email with activation key
    email_subject = _('Account confirmation')
    email_body = u"Приветб %s! Мы тут тебе отправили код подтверждения - просто пройди(кликни) по ссылке http://stage.minecraft.of.by/auth/confirm/%s не позднее чем через 48 часов. С уважением, Команда MOB сервера!" % (username, activation_key)
    args['message'] = u"На твой адрес  выслано активационное письмо - проверь свою почту и пройди по ссылке в нём, чтобы завершить регистрацию и получить свой бонус!"

    user.email_user(email_subject, email_body)
    user.set_activation_data(activation_key=activation_key, key_expires=key_expires)
    user.save()

    return render_to_response('profile.html',
                              args,
                              context_instance=RequestContext(request))

def confirm(request, activation_key):
    args = {}
    # check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        return redirect('/')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user = get_object_or_404(User, activation_key=activation_key)

    if user.is_active:
        return redirect('/')

    # check if the activation key has expired, if it hase then render confirm_expired.html
    if user.key_expires < timezone.now():
        return render_to_response('expired.html')
    # if the key hasn't expired save user and set him as active and render some template to confirm activation
    user.is_active = True
    user.save()
    args['message'] = u"Поздравляю! Ты успешно активировал свой Личный кабинет. Твои бонусные блоки будут зачислены тебе на счёт с минуты на минуту."

    return render_to_response('profile.html',
                              args,
                              context_instance=RequestContext(request))

@login_required(login_url='/auth/login/')
def profile(request):
    args = {}
    args['message'] = u"Пока что тут ничего нет"
    return render_to_response('profile.html',
                              args,
                              context_instance=RequestContext(request))
