import requests


def get_month(x):
    month_list = [
        'Января',
        'Февраля',
        'Марта',
        'Апреля',
        'Мая',
        'Июня',
        'Июля',
        'Августа',
        'Сентября',
        'Октября',
        'Ноября',
        'Декабря'
    ]

    return month_list[x-1]


def get_events():

    headers = {
        'content-type': 'application/graphql',
        'encoding': 'utf-8'
    }

    query = """
        query {
            events {
                id
                name
                description
                date
            }
        }
    """

    response = requests.get('http://127.0.0.1:8000/api/', headers=headers, params={'query': query})

    return response.json(), response.cookies.get('csrftoken')


def get_me(telegram, csrf_token):

    headers = {
        'content-type': 'application/json',
        'encoding': 'utf-8',
        'X-CSRFToken': csrf_token
    }

    cookies = {
        'csrftoken': csrf_token
    }

    query = (
            'query {'
            f'    me(telegram: "{telegram}") '
            '    {'
            '        name'
            '        faculty'
            '        group'
            '        phone'
            '    }'
            '}'
    )

    response = requests.post('http://127.0.0.1:8000/api/', headers=headers, json={'query': query}, cookies=cookies)

    return response.json()


def get_my_events(telegram):

    headers = {
        'content-type': 'application/graphql',
        'encoding': 'utf-8'
    }

    query = (
            'query {'
            f'   myEvents(telegram: "{telegram}")'
            '    {'
            '        id'
            '        name'
            '        description'
            '    }'
            '}'
    )

    response = requests.get('http://127.0.0.1:8000/api/', headers=headers, params={'query': query})

    return response.json()


def create_student(telegram, name, faculty, group, phone, event_id, csrf_token):

    headers = {
        'content-type': 'application/json',
        'encoding': 'utf-8',
        'X-CSRFToken': csrf_token
    }

    cookies = {
        'csrftoken': csrf_token
    }

    query = (
        'mutation {'
        '    createStudent(data: {'
        f'    telegram: "{telegram}", name: "{name}", faculty: "{faculty.upper()}", group: "{group.upper()}", '
        f'    phone: "{phone}"'
        '    }, event: '
        f'"{event_id}") '
        '    {'
        '        ok'
        '    }'
        '}'
    )

    response = requests.post('http://127.0.0.1:8000/api/', headers=headers, json={'query': query}, cookies=cookies)
    return response.json()


def update_student(telegram, name, faculty, group, phone, csrf_token):

    headers = {
        'content-type': 'application/json',
        'encoding': 'utf-8',
        'X-CSRFToken': csrf_token
    }

    cookies = {
        'csrftoken': csrf_token
    }

    query = (
        'mutation {'
        '    updateStudent(data: {'
        f'    telegram: "{telegram}", name: "{name}", faculty: "{faculty.upper()}", group: "{group.upper()}", '
        f'    phone: "{phone}"'
        '    }) '
        '    {'
        '        ok'
        '    }'
        '}'
    )

    response = requests.post('http://127.0.0.1:8000/api/', headers=headers, json={'query': query}, cookies=cookies)
    return response.json()


def take_part(telegram, event_id, csrf_token):

    headers = {
        'content-type': 'application/json',
        'encoding': 'utf-8',
        'X-CSRFToken': csrf_token
    }

    cookies = {
        'csrftoken': csrf_token
    }

    query = (
        'mutation {'
        '    updateStudent(data: {'
        f'    telegram: "{telegram}"'
        '    }, event: '
        f'"{event_id}") '
        '    {'
        '        ok'
        '    }'
        '}'
    )

    response = requests.post('http://127.0.0.1:8000/api/', headers=headers, json={'query': query}, cookies=cookies)
    return response.json()
