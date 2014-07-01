import multiprocessing


class ProcessPool(object):
    pool = None

    @classmethod
    def get_pool(cls):
        if cls.pool is None:
            cls.pool = multiprocessing.Pool(multiprocessing.cpu_count())
        return cls.pool
