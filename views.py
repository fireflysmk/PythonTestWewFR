from test_framework.templator import page_render


class MainPage:
    def __call__(self, request):
        return '200 OK', page_render('index.html',
                                     data=request.get('data', None))


class About:
    def __call__(self, request):
        return '200 OK', page_render('about_test_page.html',
                                     data=request.get('data', None))
