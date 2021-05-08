import quopri


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

        # находим нужный контроллер
        # отработка паттерна page controller
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound()
        request = {}
        # наполняем словарь request элементами и передаем контроллерам

        for front in self.fronts_lst:
            front(request)
        # запуск контроллера
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
