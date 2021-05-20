from datetime import date
from test_framework.templator import page_render
from patterns.сreational_patterns import Engine, Logger
from patterns.structural_patterns import AppHandlerDecoRoute, Debug

site = Engine()
logger = Logger('main')

routes = {}


@AppHandlerDecoRoute(routes=routes, url='/')
class Index():
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', page_render('index.html',
                                     objects_list=site.categories)


@AppHandlerDecoRoute(routes=routes, url='/About/')
class About:
    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', page_render('about_test_page.html',
                                     data=request.get('data', None))


@AppHandlerDecoRoute(routes=routes, url='/Reg/')
class Registry:
    @Debug(name='Registry')
    def __call__(self, request):
        return '200 OK', page_render('reg.html',
                                     data=request.get('data', None))


@AppHandlerDecoRoute(routes=routes, url='/Course/')
class Courses:
    @Debug(name='Courses')
    def __call__(self, request):
        return '200 OK', page_render('courses.html',
                                     data=request.get('data', None))


@AppHandlerDecoRoute(routes=routes, url='/courses-list/')
class CoursesList:
    @Debug(name='CoursesList')
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))

            return '200 OK', page_render('course_list.html',
                                         objects_list=category.courses,
                                         name=category.name,
                                         id=category.id
                                         )
        except KeyError:
            return '200 OK', 'There`s no courses'


@AppHandlerDecoRoute(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    @Debug(name='CreateCourse')
    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)

            return '200 OK', page_render('course_list.html',
                                         objects_list=category.courses,
                                         name=category.name, id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', page_render('create_course.html',
                                             name=category.name,
                                             id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# контроллер - создать категорию
@AppHandlerDecoRoute(routes=routes, url='/create-category/')
class CreateCategory:
    @Debug(name='CreateCategory')
    def __call__(self, request):
        print(request)
        method = request['method']
        print(f"method_type: {method}")
        if request['method'] == 'POST':
            # метод пост
            print(request)
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', page_render('index.html',
                                         objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', page_render('create_category.html',
                                         categories=categories)


# контроллер - список категорий
@AppHandlerDecoRoute(routes=routes, url='/category-list/')
class CategoryList:
    @Debug(name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', page_render('category_list.html',
                                     objects_list=site.categories)


# контроллер - копировать курс
@AppHandlerDecoRoute(routes=routes, url='/copy-course/')
class CopyCourse:
    @Debug(name='CopyCourse')
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', page_render('course_list.html',
                                         objects_list=site.courses)
        except KeyError:
            return '200 OK', 'No courses have been added yet'
