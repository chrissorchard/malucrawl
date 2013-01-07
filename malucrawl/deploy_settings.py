DEBUG = False
TEMPLATE_DEBUG = DEBUG
COMPRESS_ENABLED = True

SECRET_KEY = 'awt7_+ukgke*4h6ok0r%2x$@htbnlyu63f#5*6a5$2+@81gz0z'
BROKER_URL = "amqp://guest:mkP5b9mholFmthIixyNx@malucrawl.ecs.soton.ac.uk//"

MALUCRAWL_REDIS = {
    "master": "redis://:Km7icdOpKvb6JIzN40iG@malucrawl.ecs.soton.ac.uk:6379/0",
    "slave": "redis://:Km7icdOpKvb6JIzN40iG@localhost:6379/0"
}

CELERY_RESULT_BACKEND = MALUCRAWL_REDIS["master"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'malucrawl',                      # Or path to database file if using sqlite3.
        'USER': 'malucrawl',                      # Not used with sqlite3.
        'PASSWORD': 'tW9fZ63QeEELWt7P',                  # Not used with sqlite3.
        'HOST': 'malucrawl.ecs.soton.ac.uk',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
    'capture': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'capturehpc',                      # Or path to database file if using sqlite3.
        'USER': 'capture',
        'PASSWORD': 'capture',
        'HOST': 'kanga-toast.ecs.soton.ac.uk',
        'PORT': '',                      # Set to empty string for default.
    }
}
