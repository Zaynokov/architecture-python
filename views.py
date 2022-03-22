from new_work.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', style=request['style'])


class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html', style=request['style'])


class Examples:
    def __call__(self, request):
        return '200 OK', render('examples.html', style=request['style'])


class Page:
    def __call__(self, request):
        return '200 OK', render('page.html', style=request['style'])


class AnotherPage:
    def __call__(self, request):
        return '200 OK', render('another_page.html', style=request['style'])
