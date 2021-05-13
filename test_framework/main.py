import quopri
from test_framework.requests import GetRequests, PostRequests


class PageNotFound:
    def __call__(self, request):
        return '404 Error', '404 PAGE Not Found'


class Framework:
    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        request = {}

        request_type = environ['REQUEST_METHOD']
        request['method'] = request_type

        if request_type == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = data
            print(f'выполнен post-запрос: '
                  f'{Framework.decode_value(data)}'
                  )
        if request_type == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = request_params
            print(f'выполнен get-запрос: '
                  f'{request_params}'
                  )

        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound()

        # наполняем словарь request элементами и передаем контроллерам

        for front in self.fronts_lst:
            front(request)
        # запуск контроллера
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        parse_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            parse_data[k] = val_decode_str
        return parse_data
