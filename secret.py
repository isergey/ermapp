# -*- coding: utf-8 -*-

DEV = {
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            #'NAME': 'base.db', # Or path to database file if using sqlite3.
            'NAME': 'erm', # Or path to database file if using sqlite3.
            'USER': 'root', # Not used with sqlite3.
            'PASSWORD': '123456', # Not used with sqlite3.
            'HOST': '127.0.0.1', # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306', # Set to empty string for default. Not used with sqlite3.
#            'OPTIONS': {
#                'init_command': 'SET storage_engine=INNODB',
#                }
        }

#        'default': {
#            'ENGINE': 'django.db.backends.postgresql_psycopg2',
#            # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#            #'NAME': 'base.db', # Or path to database file if using sqlite3.
#            'NAME': 'erm', # Or path to database file if using sqlite3.
#            'USER': 'postgres', # Not used with sqlite3.
#            'PASSWORD': '123456', # Not used with sqlite3.
#            'HOST': '127.0.0.1', # Set to empty string for localhost. Not used with sqlite3.
#            'PORT': '5432', # Set to empty string for default. Not used with sqlite3.
#        }
    },

    'CACHES': {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake'
            }
    },

    'SECRET_KEY': '6e&h!4$+&p+!@^543%jn&+x!j3g-pf3%%frsvo2=6p*&*eo_i)'

}

PROD = {
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'base.db', # Or path to database file if using sqlite3.
            'USER': '', # Not used with sqlite3.
            'PASSWORD': '', # Not used with sqlite3.
            'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '', # Set to empty string for default. Not used with sqlite3.

        }
    },

    'CACHES': {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/tmp/django_cache',
            }
    },
    
    'SECRET_KEY': '6e&h!4$+&p+!@^543%jn&+x!j3g-pf3%%frsvo2=6p*&*eo_i)'

}