from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# from django.contrib import databrowse
# from arena.models import Question
# from accounts.models import Team, Player
# databrowse.site.register(Question)
# databrowse.site.register(Team)
# databrowse.site.register(Player)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cqa.views.home', name='home'),
    # url(r'^cqa/', include('cqa.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^matrix/', include(admin.site.urls)),

    # (r'^databrowse/(.*)', databrowse.site.root),

    (r'^$', 'arena.views.index'),
    (r'^board/$', 'arena.views.board'),
    (r'^hack/$', 'arena.views.hack'),
    (r'^questions/$', 'arena.views.get_questions'),
    (r'^leaders/$', 'arena.views.get_leaders'),
    (r'^login/$', 'accounts.views.log_in'),
    (r'^logout/$', 'accounts.views.log_out'),
    (r'^register/$', 'accounts.views.register'),
)

urlpatterns += staticfiles_urlpatterns()
