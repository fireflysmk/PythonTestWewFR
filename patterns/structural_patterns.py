from time import time


# структурный паттерн - Декоратор
class AppHandlerDecoRoute:
    def __init__(self, routes, url):
        '''
        Сохраняем значение переданного параметра для словаря routes
        и конкретного пути - url
        т.е. наполняем словарь всеми путями при импорте класса
        '''
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


# паттер Декоратор, для наших views
class Debug:

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        # подсчет времени выполнения
        def timeit(method):
            '''
            нужен для того, чтобы декоратор класса wrapper обернул в timeit
            каждый метод декорируемого класса
            '''
            def timed(*args, **kw):
                time_start = time()
                result = method(*args, **kw)
                time_end = time()
                delta = time_end - time_start

                print(f'debug --> {self.name} выполнялся {delta:2.2f} ms')
                return result

            return timed

        return timeit(cls)
