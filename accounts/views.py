# Create your views here.

from hashlib import sha1
from datetime import datetime

from django.conf import settings
from django.http import Http404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import ugettext as _

from cqa.accounts.models import Team
from cqa.accounts.forms import RegisterForm, LogInForm

def get_hash(raw):
    import random
    salt = sha1(str(random.random()) + str(random.random())).hexdigest()[:5]
    hash_result = sha1(salt + raw.encode('utf-8')).hexdigest()
    return '%s$%s$%s' % ('sha1', salt, hash_result)

def register(request):
    if request.user.is_authenticated():
        return redirect('/board')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            team_name = form.cleaned_data['team_name']

            # Get or create team.
            import re
            m = re.search(r'^sha1\$[a-z0-9]{5}\$[a-z0-9]{40}$', team_name)
            if m is not None:
                team = get_object_or_404(Team, name_hash=team_name)
            else:
                team = Team.objects.create(name=team_name, name_hash=get_hash(team_name))

            # Create new user.
            user = User.objects.create_user(username, email, password)
            u = authenticate(username=username, password=password)
            login(request, u)

            player = user.get_profile()
            player.team = team
            player.save()

            try:
                template_values = {
                    'username': username,
                    'team_name': team.name,
                    'name_hash': team.name_hash,
                    'organizer': settings.CQA_ORGANIZER
                }
                message = render_to_string('email_template.html', template_values)
                send_mail(_('Registration Successful'), message, 'noreply@myclover.org', [email])
            except BadHeaderError:
                raise Http404

            return redirect('/board')
    else:
        form = RegisterForm()

    return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))

def log_in(request):
    if request.method != 'POST':
        raise Http404

    error = None
    form = LogInForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_superuser:
                raise Http404

            if user.is_active:
                today = datetime.today()
                request.session.set_expiry(datetime(today.year, today.month+1, today.day))
                login(request, user)
                return redirect('/board')
            else:
                raise Http404
        else:
            error = _("Your username and password were incorrect.")

    return render_to_response('index.html', {'form': form, 'error': error}, context_instance=RequestContext(request))

def log_out(request):
    logout(request)
    return redirect('/')
