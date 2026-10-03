from time import time


class TimerStatus:
    running = "running"
    stopped = "stopped"


def get_now_ms() -> int:
    return int(time() * 1000)
