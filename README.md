# Django Terralego

[![Build Status](https://travis-ci.org/makinacorpus/django-terralego.svg?branch=master)](https://travis-ci.org/makinacorpus/django-terralego) [![Documentation Status](https://readthedocs.org/projects/django-terralego/badge/?version=latest)](http://django-terralego.readthedocs.io/en/latest/?badge=latest)

## Getting started

Install django-terralego:

```shell
$ pip install django-terralego
```

Configure terralego by updating your `settings.py`:

```python
TERRALEGO = {
    'USER': 'user',
    'PASSWORD': 'password',
}
```

You can disabled the requests made to terralego by setting the terrelago `ENABLED` setting to `False`:

```python
TERRALEGO = {
    'ENABLED': False,
}
```


## Exceptions

In case of errors, the exceptions raised are the one from [requests](http://docs.python-requests.org/en/master/user/quickstart/#errors-and-exceptions).