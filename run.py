from test_framework.main import Framework
from wsgiref.simple_server import make_server
from urls import fronts
from views import routes

application = Framework(routes, fronts)

with make_server('', 8090, application) as httpd:
    print("Запуск на порту 8080...")
    httpd.serve_forever()
