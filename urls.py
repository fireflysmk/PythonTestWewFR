from datetime import date
from views import MainPage, About


def data_front(request):
    request['data'] = date.today()

def key_front(request):
    request['key'] = 'key'


fronts = [data_front, key_front]

routes = {
    '/': MainPage(),
    '/about/': About(),
}
