from .base import *

DEBUG = False

ALLOWED_HOSTS = ['tm30-api.herokuapp.com']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd1l1lbhpvkacpn',
        'USER': 'zxlnocxvotovgn',
        'PASSWORD': 'c40b038eaa2781d975f4ccb63cce39876f9a339e46bee342bdb1227232d13e75',
        'HOST': 'ec2-54-175-79-57.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}
