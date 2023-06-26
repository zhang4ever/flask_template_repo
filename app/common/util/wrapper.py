import threading
import time


import time


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print('Total time cost: {:.5f} s'.format(time.time() - start))
        return res
    return wrapper


def exception_handler(logger, default_return=None):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(f'Error occurs in function [{func.__name__}], error: {str(e)}')
                return default_return
        return inner_wrapper
    return wrapper


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

