from new_work.templator import render
from patterns.creation_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug

site = Engine()
logger = Logger('main')

routes = {}


@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html',
                                categories=site.categories)


@AppRoute(routes=routes, url='/contact')
class Contact:
    @Debug(name='Contact')
    def __call__(self, request):
        return '200 OK', render('contact.html')


@AppRoute(routes=routes, url='/personal_page')
class PersonalPage:
    @Debug(name='PersonalPage')
    def __call__(self, request):
        return '200 OK', render('personal_page.html')


@AppRoute(routes=routes, url='/registration')
class Registration:
    @Debug(name='Registration')
    def __call__(self, request):
        return '200 OK', render('registration.html')


@AppRoute(routes=routes, url='/courses')
class CoursesList:
    @Debug(name='CoursesList')
    def __call__(self, request):
        logger.log('Список курсов')
        categories = site.categories
        return '200 OK', render('courses.html',
                                objects_list=categories,
                                courses_dict=site.courses_dict)


@AppRoute(routes=routes, url='/new_course')
class NewCourse:
    @Debug(name='NewCourse')
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост
            data = request['data']
            name = data['name']
            category = data['category']
            course_type = data['type']

            course_type = site.decode_value(course_type)
            category = site.decode_value(category)
            name = site.decode_value(name)

            new_course = site.create_course(course_type, name, category)

            temp_list = site.courses_dict[category]
            temp_list.append(new_course)
            site.courses_dict.update({category: temp_list})

            categories = site.categories
            print(request)
            return '200 OK', render('courses.html',
                                    objects_list=categories,
                                    courses_dict=site.courses_dict)
        else:
            categories = site.categories
            return '200 OK', render('new_course.html',
                                    objects_list=categories)


@AppRoute(routes=routes, url='/new_category')
class NewCategory:
    @Debug(name='NewCategory')
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category_id = data.get('category_id')
            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)
            site.categories.append(new_category)
            categories = site.categories
            site.courses_dict[name] = []
            return '200 OK', render('courses.html',
                                    objects_list=categories,
                                    courses_dict=site.courses_dict)
        else:
            return '200 OK', render('new_category.html')


@AppRoute(routes=routes, url='/edit')
class Editor:
    @Debug(name='Editor')
    def __call__(self, request):
        return '200 OK', render('edit.html',
                                objects_list=site.categories,
                                courses_dict=site.courses_dict
                                )


class EditCourse:
    pass


class EditCategory:
    pass
