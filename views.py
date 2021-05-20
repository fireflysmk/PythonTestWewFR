from patterns.сreational_patterns import Engine, Logger, MapperRegistry
from patterns.structural_patterns import AppHandlerDecoRoute, Debug
from patterns.behavioral_patterns import *
from patterns.sys_unit_of_work_pattern import UnitOfWork

from test_framework.templator import page_render

site = Engine()
logger = Logger('main')

email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

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

@AppHandlerDecoRoute(routes=routes, url='/ForStudents/')
class ForStudents:
    @Debug(name='ForStudents')
    def __call__(self, request):
        return '200 OK', page_render('for_students.html',
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
                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)
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
            return '200 OK', 'there`s no course'


@AppHandlerDecoRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()



@AppHandlerDecoRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


@AppHandlerDecoRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@AppHandlerDecoRoute(routes=routes, url='/student-list/')
class StudentListView(ListView):
    template_name = 'student_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.all()
