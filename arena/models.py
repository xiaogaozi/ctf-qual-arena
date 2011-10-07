from django.db import models
from djangotoolbox.fields import ListField
from django.utils.translation import ugettext_lazy as _

# Create your models here.

CATEGORY_CHOICES = (
    (1, 'Grab Bag'),
    (2, 'Retro Revisited'),
    (3, 'Binary L33tness'),
    (4, 'Pwtent Pwnables'),
    (5, 'Forensics')
)

SCORE_CHOICES = (
    (100, '100'),
    (200, '200'),
    (300, '300'),
    (400, '400'),
    (500, '500')
)

STATUS_CHOICES = (
    ('close', _('Close')),
    ('open', _('Open'))
)

class Question(models.Model):
    category = models.IntegerField(_('category'), choices=CATEGORY_CHOICES)
    score = models.IntegerField(_('score'), choices=SCORE_CHOICES)
    desc = models.TextField(_('description'))
    answer = models.CharField(_('answer'), max_length=100)
    status = models.CharField(_('status'), max_length=5, choices=STATUS_CHOICES, default='close')
    resolved_teams = ListField(verbose_name=_('Resolved Teams'), blank=True, editable=False)
