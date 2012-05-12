This project is an imitation of [DEF CON](https://www.defcon.org/) platform, since I didn't find any implementation. The orignal platform is written in Java, this project is purely Python powered with [Django](https://www.djangoproject.com/) framework.

# Requirements #

- Python 2.6 or later
- [Django-nonrel](http://www.allbuttonspressed.com/projects/django-nonrel)
- [djangotoolbox](http://www.allbuttonspressed.com/projects/djangotoolbox)
- [MongoDB](http://www.mongodb.org/)
- [Django MongoDB Engine](http://django-mongodb.org/)

It's highly recommended (although not required) to use a [virtualenv](http://virtualenv.org/) for your project to not mess up other Django setups.

# Bootstrap #

Clone CQA repository, note that directory name must be "cqa", cause it's also the Python package name.

```bash
$ git clone git://github.com/xiaogaozi/ctf-qual-arena.git cqa
```

Create a temporary Django project to get the `SECRET_KEY` in `settings.py`, and replace the same setting in `cqa/settings.py`.

```bash
$ django-admin.py startproject tempproject
$ grep 'SECRET_KEY' tempproject/settings.py
```

Replace `/path/to/cqa` in `cqa/settings.py` with your curreny path.

If you use Mac OS, use this command:

```bash
$ sed -i '' "s%/path/to/cqa%$(pwd)/cqa%g" cqa/settings.py
```

Linux user use this command:

```bash
$ sed -i "s%/path/to/cqa%$(pwd)/cqa%g" cqa/settings.py
```

Setup SMTP server settings, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`.

Edit `CQA_ORGANIZER` to whatever you wanted, this setting will be used as the Email signature.

Now run `syncdb`:

```bash
$ cd cqa
$ python manage.py syncdb
```

Use MongoDB shell to get `SITE_ID`, then fill in `cqa/settings.py` file. Note: everytime you drop Django database, you should repeat this step again.

```bash
$ mongo
> use cqa
switched to db cqa
> db.django_site.find()
{ "_id" : ObjectId("4e8210f6ae990052bf00001e"), "domain" : "example.com", "name" : "example.com" }
```

# Deployment #

## Apache and mod_wsgi ##

Example Apache configurations:

```apache
# Alias /robots.txt /path/to/cqa/static/robots.txt
# Alias /favicon.ico /path/to/cqa/static/images/favicon.ico

AliasMatch ^/([^/]*\.css) /path/to/cqa/static/stylesheets/$1

Alias /static/ /path/to/cqa/static/

<Directory /path/to/cqa/static>
    Order deny,allow
    Allow from all
</Directory>

WSGIScriptAlias / /path/to/cqa/apache/django.wsgi

<Directory /path/to/cqa/apache>
    Order deny,allow
    Allow from all
</Directory>
```

For more information, please visit [How to use Django with Apache and mod_wsgi](https://docs.djangoproject.com/en/1.3/howto/deployment/modwsgi/) and [Integration With Django](http://code.google.com/p/modwsgi/wiki/IntegrationWithDjango).

If you use virtualenv, you should follow [instructions](http://code.google.com/p/modwsgi/wiki/VirtualEnvironments#Baseline_Environment) to create a baseline Python environment. Then add following line to Apache configuration file.

```apache
WSGIPythonHome /path/to/virtualenv/BASELINE
```

Replace `/path/to/virtualenv` and `/path/to/cqa` in `cqa/apache/django.wsgi` file with correct path.

To serve admin static files, create a symbol link in `cqa/static` directory.

```bash
$ cd cqa/static
$ ln -s /path/to/django/contrib/admin/media admin
```

# Development #

Just run Django development server:

```bash
$ python manage.py runserver
```

# Security #

By default, the Django admin is enabled. If you want to disable it, just comment those lines in `settings.py` and `urls.py`.

MongoDB default is running without security, if you consider this problem, please read the official [documentation](http://www.mongodb.org/display/DOCS/Security+and+Authentication).

# Getting involved #

CTF Qual Arena currently contains only two languages: English and Simplified Chinese. Translation is always welcome. With Django i18n support, it's very easy to translate into a new language. Create `.po` file, translate, submit your `.po` file. The following instructions is an example how to create `.po` file. Django will automatically create it in +cqa/locale+ directory. For more language identifiers, please visit http://www.i18nguy.com/unicode/language-identifiers.html.

```bash
$ cd cqa
$ django-admin.py makemessages -l fr-FR
```

It's recommended to use [Poedit](http://www.poedit.net/) to edit the `.po` file, but you may use your favorite editor freely.
