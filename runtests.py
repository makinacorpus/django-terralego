#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_terralego.tests.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    tests = ['django_terralego.tests'] if len(sys.argv) == 1 else sys.argv[1:]
    failures = test_runner.run_tests(tests)
    sys.exit(bool(failures))
