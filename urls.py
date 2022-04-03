from views import Index, Contact, PersonalPage, Registration, NewCategory, NewCourse, CoursesList, Editor


# front controller
def styling(request):
    pass


def other_front(request):
    request['key'] = 'key'


fronts = [styling, other_front]

routes = {
    '/': Index(),
    '/contact/': Contact(),
    '/personal_page/': PersonalPage(),
    '/courses/': CoursesList(),
    '/registration/': Registration(),
    '/new_category/': NewCategory(),
    '/new_course/': NewCourse(),
    '/edit/': Editor()
}
