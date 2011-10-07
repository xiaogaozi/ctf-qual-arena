from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from cqa.accounts.models import Team

class UsernameField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(UsernameField, self).__init__(max_length=30, *args, **kwargs)

    def validate(self, value):
        """Check if user is existed."""
        super(UsernameField, self).validate(value)
        if User.objects.filter(username=value).count() != 0:
            raise forms.ValidationError(_('Username is existed.'))

class PasswordField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(PasswordField, self).__init__(min_length=8, *args, **kwargs)

class TeamNameField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(TeamNameField, self).__init__(max_length=51, *args, **kwargs)

    def validate(self, value):
        """Check if user is existed."""
        super(TeamNameField, self).validate(value)
        if Team.objects.filter(name=value).count() != 0:
            raise forms.ValidationError(_('Team name is existed.'))

class RegisterForm(forms.Form):
    username = UsernameField(label=_('Username'))
    password = PasswordField(label=_('Password'))
    email = forms.EmailField(label=_('Email'))
    team_name = TeamNameField(label=_('Team name'))

class LogInForm(forms.Form):
    username = forms.CharField(label=_('Username'))
    password = forms.CharField(label=_('Password'))
