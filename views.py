from new_work.templator import render
from patterns.creation_patterns import Engine, Logger

site = Engine()
logger = Logger('main')


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html',
                                categories=site.categories)


class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html')


class PersonalPage:
    def __call__(self, request):
        return '200 OK', render('personal_page.html')


class Registration:
    def __call__(self, request):
        return '200 OK', render('registration.html')


class CoursesList:
    def __call__(self, request):
        logger.log('Список курсов')
        categories = site.categories
        return '200 OK', render('courses.html',
                                objects_list=categories,
                                courses_dict=site.courses_dict)


# контроллер - создать курс
class NewCourse:
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


# контроллер - создать категорию
class NewCategory:
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


class Editor:
    def __call__(self, request):
        return '200 OK', render('edit.html',
                                objects_list=site.categories,
                                courses_dict=site.courses_dict
                                )


class EditCourse:
    pass


class EditCategory:
    pass


# контроллер - копировать курс
class CopyCourse:
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

            return '200 OK', render('course_list.html',
                                    objects_list=site.courses,
                                    name=new_course.category.name)
        except KeyError:
            return '200 OK', 'No courses have been added yet'
