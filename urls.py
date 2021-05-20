from datetime import date
from views import *


def data_front(request):
    request['date'] = date.today()


def key_front(request):
    request['key'] = 'key'


fronts = [data_front, key_front]

"""
remove this and replace by deco-logic -> structural_patters logic

routes = {
    '/': Index(),
    '/About/': About(),
    '/Reg/': Registry(),
    '/Course/': Courses(),
    '/courses-list/': CoursesList(),
    '/create-course/': CreateCourse(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList(),
    '/copy-course/': CopyCourse()
}
"""