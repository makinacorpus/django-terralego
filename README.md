# Terralego

## Getting started

Install the terralego python binding:

```shell
$ pip install terralego
```

You need to set the configuration before using the different methods:

```python
from terralego.conf import settings

settings.USER = 'my_user'
settings.PASSWORD = 'my_password'
```

Alternatively, you can set the `TERRALEGO_USER` and `TERRALEGO_PASSWORD` environment variables.

You can now use the terralego services, for example:

```python
from terralego.geodirectory import create_entry

entry_id = create_entry('POINT(47.2556155 -1.5364181)', ["city", "nantes"])
```


## Exceptions

In case of errors, the exceptions raised are the one from [requests](http://docs.python-requests.org/en/master/user/quickstart/#errors-and-exceptions).