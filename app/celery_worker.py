from celery import Celery, signals
import time
import functools


def make_celery(app_name=__name__):
    backend = broker = 'redis://test_redis:6377/0'
    return Celery(app_name, backend=backend, broker=broker)


celery = make_celery()


def time_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        exec_time = end_time - start_time
        return (result, exec_time)

    return wrapper


@celery.task
@time_decorator
def generate_task(time_in_s):
    print(f"Sleep for {time_in_s}")
    time.sleep(time_in_s)
    return time_in_s


def get_active_tasks():
    # Inspect all nodes.
    i = celery.control.inspect()
    # Show tasks that are currently active.
    active_tasks = i.active()
    return active_tasks


def get_scheduled_tasks():
    # Inspect all nodes.
    i = celery.control.inspect()
    # Show tasks that are currently scheduled.
    active_tasks = i.scheduled()
    return active_tasks
