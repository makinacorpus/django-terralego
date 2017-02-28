from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='django-terralego',
    version='0.1',
    description='Django mixins for Terralego services.',
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    url='https://terralego.fr',
    author='Autonomens',
    author_email='contact@autonomens.fr',
    license='MIT',
    packages=['django_terralego'],
    install_requires=[
        'terralego==0.1',
        'Django',
        'django-leaflet==0.21.0',
        'django-geojson[field]==2.10.0',
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False,
)
