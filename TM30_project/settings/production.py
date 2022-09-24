from .base import *

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd84bei8buppmau',
        'USER': 'hxtshipeqmkuxq',
        'PASSWORD': 'f1bb1a5cf0f07a1e6b825dad7fcd040f34ba1930359b74bbda86e223128cb0ad',
        'HOST': 'ec2-52-200-5-135.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}