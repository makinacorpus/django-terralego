# Django Terralego

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


## Exceptions

In case of errors, the exceptions raised are the one from [requests](http://docs.python-requests.org/en/master/user/quickstart/#errors-and-exceptions).