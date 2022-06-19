import threading


def singleton(cls):
    """
    使用加锁的方式实现单例模式，线程安全
    """
    instances = {}
    lock = threading.Lock()

    def _singleton(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton



