from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls

from view import welcome, that_day, another_day, today


routes = [
    Route('/', 'GET', welcome),
    Route('/oneday/today', 'GET', today),
    Route('/oneday/{date_string}', 'GET', that_day),
    Route('/oneday/{date_string}/{opt}', 'GET', another_day),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]

app = App(routes=routes)


if __name__ == '__main__':
    app.main()
