DEBUG = True
TEMPLATE_DEBUG = DEBUG
COMPRESS_ENABLED = True

SECRET_KEY = 'awt7_+ukgke*4h6ok0r%2x$@htbnlyu63f#5*6a5$2+@81gz0z'
BROKER_URL = "amqp://guest:mkP5b9mholFmthIixyNx@malucrawl.ecs.soton.ac.uk//"

CElERY_IMPORTS = ("malware_crawl.tasks",)

MALUCRAWL_REDIS = {
    "master": "redis://:Km7icdOpKvb6JIzN40iG@malucrawl.ecs.soton.ac.uk:6379/0",
    "slave": "redis://:Km7icdOpKvb6JIzN40iG@localhost:6379/0"
}

CELERY_RESULT_BACKEND = MALUCRAWL_REDIS["master"]
