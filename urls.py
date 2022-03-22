from views import Index, Contact, Examples, Page, AnotherPage


# front controller
def styling(request):
    with open('templates/style/style.css', encoding='utf-8') as f:
        style = f.read()
        request['style'] = style


def other_front(request):
    request['key'] = 'key'


fronts = [styling, other_front]

routes = {
    '/': Index(),
    '/contact/': Contact(),
    '/examples/': Examples(),
    '/page/': Page(),
    '/another_page/': AnotherPage(),
}
