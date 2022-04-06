from views import Index, Contact, PersonalPage, Registration, NewCategory, NewCourse, CoursesList, Editor


# front controller
def styling(request):
    pass


def other_front(request):
    request['key'] = 'key'


fronts = [styling, other_front]

