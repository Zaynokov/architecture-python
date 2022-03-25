from quopri import decodestring
import datetime

from new_work.requests import GetRequests, PostRequests


class PageNotFound404:
    def __call__(self, request):
        return '404 Error', '404 Page Not Found'


class Framework:
    """Класс Framework - основа фреймворка"""

    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):
        # получаем адрес, по которому выполнен переход
        path = environ['PATH_INFO']
        method = environ['REQUEST_METHOD']
        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'
        request = {'method': method}
        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = Framework.decode_value(request_params)
            with open('get_data.txt', 'a', encoding='utf-8') as file:
                file.write(str(datetime.datetime.now()) + ' ' + str(request['request_params']) + '\n') \
                    if request['request_params'] else None
        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = Framework.decode_value(data)
            with open('post_data.txt', 'a', encoding='utf-8') as file:
                file.write(str(datetime.datetime.now()) + ' ' + str(request['data']) + '\n') \
                    if request['data'] else None

        # находим нужный контроллер
        # отработка паттерна page controller
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()

        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # отработка паттерна front controller
        for front in self.fronts_lst:
            front(request)
        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        result = {}
        for key, value in data.items():
            val = bytes(value.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            result[key] = val_decode_str
        return result
