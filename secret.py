# -*- coding: utf-8 -*-

DEV = {
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

    'SECRET_KEY': '6e&h!4$+&p+!@^543%jn&+x!j3g-pf3%%frsvo2=6p*&*eo_i)'

}