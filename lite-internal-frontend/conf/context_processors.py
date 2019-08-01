import os


def export_vars(request):
    return {'ENVIRONMENT_VARIABLES': dict(os.environ.items())}


def lite_menu(request):
    return {
        'LITE_MENU': [
            {
                'title': 'Cases',
                'url': '/cases/',
                'icon': 'menu/cases'
            },
            {
                'title': 'Organisations',
                'url': '/organisations/',
                'icon': 'menu/businesses'
            },
            {
                'title': 'Teams',
                'url': '/teams/',
                'icon': 'menu/teams'
            },
            {
                'title': 'My Team',
                'url': '/team',
                'icon': 'menu/teams'
            },
            {

                'title': 'Queues',
                'url': '/queues/',
                'icon': 'menu/queues'
            },
            {
                'title': 'Users',
                'url': '/users/',
                'icon': 'menu/users'
            },
            {
                'title': 'Flags',
                'url': '/flags/',
                'icon': 'menu/flags'
            }
        ]
    }
