# Create your views here.

import json
from datetime import datetime

from django.http import Http404, HttpResponse
from django.contrib import messages
from django.template import RequestContext
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.utils.translation import ugettext as _

from cqa.arena.models import Question
from cqa.arena.forms import HackForm
from cqa.accounts.models import Team
from cqa.accounts.forms import LogInForm

def index(request):
    if request.user.is_authenticated():
        return redirect('/board')

    form = LogInForm()
    return render_to_response('index.html', {'form': form}, context_instance=RequestContext(request))

def board(request):
    if not request.user.is_authenticated():
        return redirect('/')
    if request.user.is_superuser:
        raise Http404

    message = None
    storage = messages.get_messages(request)
    for msg in storage:
        message = msg

    player = request.user.get_profile()
    return render_to_response('board.html', {'player': player, 'message': message}, context_instance=RequestContext(request))

def get_questions(request):
    if not request.user.is_authenticated() or request.user.is_superuser:
        raise Http404

    resolved = request.user.get_profile().team.resolved.split(',')

    questions = []
    for score in [100, 200, 300, 400, 500]:
        qlist = []
        q_objects = Question.objects.filter(score=score).order_by('category')
        if q_objects:
            for q in q_objects:
                d = {'score': q.score, 'desc': '', 'id': '', 'class': q.status}
                if q.status == 'open':
                    d['desc'] = q.desc
                    d['id'] = '%d:%d' % (q.category, q.score)
                    if d['id'] in resolved:
                        d['class'] = ' '.join([d['class'], 'resolved'])
                qlist.append(d)
        questions.append(qlist)

    return HttpResponse(json.dumps(questions), mimetype='application/json')

def get_leaders(request):
    if not request.user.is_authenticated() or request.user.is_superuser:
        raise Http404

    leaders = list(Team.objects.exclude(score=0).order_by('-score').values('name', 'score'))[:15]
    return HttpResponse(json.dumps(leaders), mimetype='application/json')

def hack(request):
    if request.method != 'POST' or not request.user.is_authenticated() or request.user.is_superuser:
        raise Http404

    form = HackForm(request.POST)
    if not form.is_valid():
        raise Http404

    # Ensure the interval between two most recent requests
    # less than 10 seconds. Otherwise, prevent this request.
    now = datetime.now()
    if request.session.get('last_request', False):
        delta = now - request.session['last_request']
        request.session['last_request'] = now
        # Check whether the interval between two most recent
        # requests less than 10 seconds.
        if delta.seconds < 10:
            messages.error(request, _("Oops, you request too fast."))
            return redirect('/board')
    else:
        # The first request
        request.session['last_request'] = now

    category, score = form.cleaned_data['q_id'].split(':')
    answer = form.cleaned_data['answer']

    question = get_object_or_404(Question, category=category, score=score, status='open')

    if question.answer == answer:
        team = request.user.get_profile().team
        resolved = team.resolved.split(',')
        if not form.cleaned_data['q_id'] in resolved:
            team.score += question.score
            team.resolved = ','.join([team.resolved, form.cleaned_data['q_id']]).strip(',')
            team.save()

            question.resolved_teams.append(team.name)
            question.save()

        messages.success(request, _("Yeah! You have the world."))
    else:
        messages.error(request, _("Dude, are you a newbie?"))

    return redirect('/board')
