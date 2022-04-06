from time import time


class AppRoute:

    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        if not self.url.endswith('/'):
            self.url = f'{self.url}/'
        self.routes[self.url] = cls()


class Debug:

    def __init__(self, name):

        self.name = name

    def __call__(self, cls):

        def timeit(method):
            def timed(*args, **kw):
                time_before = time()
                result = method(*args, **kw)
                time_after = time()
                time_delta = time_after - time_before
                print(f'Время выполнения {self.name} составляет {time_delta:2.2f} ms')
                return result

            return timed

        return timeit(cls)
