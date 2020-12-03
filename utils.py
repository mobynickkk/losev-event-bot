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
                start_of_registration_datetime
                end_of_registration_datetime
            }
        }
    """

    response = requests.get('http://35.158.11.40/api/', headers=headers, params={'query': query})

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

    response = requests.post('http://35.158.11.40/api/', headers=headers, json={'query': query}, cookies=cookies)

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

    response = requests.get('http://35.158.11.40/api/', headers=headers, params={'query': query})

    return response.json()


def create_student(telegram, student_id, faculty, group, event_id, csrf_token):

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
        f'     telegram: "{telegram}", studentId: "{student_id}", faculty: "{faculty.upper()}", '
        f'     group: "{group.upper()}"'
        '    }, event: '
        f'     "{event_id}") '
        '    {'
        '        ok'
        '    }'
        '}'
    )

    response = requests.post('http://35.158.11.40/api/', headers=headers, json={'query': query}, cookies=cookies)
    return response.json()


def update_student(telegram, student_id, faculty, group, csrf_token):

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
        f'    telegram: "{telegram}", studentId: "{student_id}", faculty: "{faculty.upper()}", '
        f'    group: "{group.upper()}"'
        '    }) '
        '    {'
        '        ok'
        '    }'
        '}'
    )

    response = requests.post('http://35.158.11.40/api/', headers=headers, json={'query': query}, cookies=cookies)
    return response.json()


def is_member(student_id, csrf_token):
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
        '    isMember('
        f'    studentId: "{student_id}")'
        '    {'
        '        membership'
        '    }'
        '}'
    )

    response = requests.get('http://35.158.11.40/api/', headers=headers, json={'query': query}, cookies=cookies)

    return response.json().get('data').get('isMember').get('membership')


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

    response = requests.post('http://35.158.11.40/api/', headers=headers, json={'query': query}, cookies=cookies)
    return response.json()


def create_application(student_id, event_id, csrf_token):
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
        '    createApplication(data: {'
        f'     studentId: "{student_id}", event: "{event_id}")'
        '    {'
        '        ok'
        '    }'
        '}'
    )

    response = requests.post('http://35.158.11.40/api/', headers=headers, json={'query': query}, cookies=cookies)
    return response.json()


def create_application_for_new_user(telegram, student_id,
                                    faculty, group,
                                    event_id, csrf_token):
    student = create_student(telegram, student_id, faculty, group, event_id, csrf_token)

    if student:
        application = create_application(student_id, event_id, csrf_token)
        return application

    return {'data': None}
