from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Team(models.Model):
    name = models.CharField(_('name'), max_length=51, editable=False, unique=True)
    name_hash = models.CharField(max_length=51, editable=False, unique=True)
    score = models.IntegerField(_('score'), default=0, editable=False)
    # Resolved questions, comma separated, format like
    # this (category:score): 1:100,2:300,5:200
    resolved = models.CharField(_('Resolved Questions'), max_length=200, editable=False)

class Player(models.Model):
    user = models.ForeignKey(User, unique=True)
    team = models.ForeignKey(Team, null=True, default=None)

def create_profile(sender, **kwargs):
    user = kwargs['instance']
    if kwargs['created']:
        player = Player(user=user)
        player.save()

post_save.connect(create_profile, sender=User, dispatch_uid="profile_unique_identifier")
