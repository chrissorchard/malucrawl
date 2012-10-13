from celery import Celery, group

celery = Celery('tasks', backend='redis://:Km7icdOpKvb6JIzN40iG@kanga-cso1g09c', broker='amqp://guest:mkP5b9mholFmthIixyNx@kanga-cso1g09c//')

@celery.task
def add(x, y):
    return x + y

@celery.task
def addlist(list):
    return group(add.subtask((i,i)) for i in list).apply_async()

