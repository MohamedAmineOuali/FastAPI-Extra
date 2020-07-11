from typing import Callable

startup = []
shutdown = []


def on_startup(func: Callable):
    startup.append(func)
    return func


def on_shutdown(func: Callable):
    shutdown.append(func)
    return func
