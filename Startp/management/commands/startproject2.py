import os
import re

from django.core.management.commands import startproject


class Command(startproject.Command):
    help = 'Starts the project'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

        parser.add_argument('app')
        parser.add_argument('settings')

        parser.add_argument(
            '--app',
            dest='app_name',
            action='store_true',
        )
        parser.add_argument(
            '--c_settings',
            dest='settings',
            action='store_true'
        )

    def handle(self, *args, **options):
        project_name = options.get('name')
        super(Command, self).handle(**options)
        os.chdir(project_name)
        self.create_venv()
        print(options.get('app'))
        app_name = options.get('app')
        if app_name:
            self.create_apps(app_name)
            print('success')
            print('ssssss', options.get('settings'))
            if options.get('settings'):
                self.handle_settings(project_name, app_name)

    @staticmethod
    def create_venv():
        # create a virtual environment with venv
        # TODO name for venv
        print('Creating virtual environment...')
        os.system(f'python3 -m venv env')
        print(f'Created virtual environment: env')

    def create_apps(self, app_name):
        os.system(f'python manage.py startapp {app_name}')

        # create templates folder structure
        os.makedirs(os.path.join(app_name, 'templates'), exist_ok=True)
        os.makedirs(os.path.join(app_name, 'templates', app_name), exist_ok=True)
        self.modify_views_py(app_name)
        self.create_urls_py(app_name)

    @staticmethod
    def modify_views_py(app_name):
        """
        Rewrite the respective 'views.py' file from the current django app
        with a basic function view called '{app_name}_starter', which returns
        a <h1> HTML element as its response.

        Parameter:
        - app_name(str): the django app name.

        Return:
        - None
        """
        with open(os.path.join(app_name, 'views.py'), 'w') as file:
            views_file_content = (
                'from django.http import HttpResponse\n\n\n'
                f'def {app_name}_starter(request):\n'
                f'    return HttpResponse("<h1>{app_name.upper()} PAGE</h1>")\n'
            )
            file.write(views_file_content)

    @staticmethod
    def create_urls_py(app_name):
        """
        Create a 'urls.py' file inside the folder from the current django app
        with a route named '{app_name}_all'. This '{app_name}/urls.py' file will be included
        in the entrypoint '{project_name}/urls.py' later.

        Parameter:
        - app_name(str): the django app name.

        Return:
        - None
        """

        urls_file_content = ('from django.urls import path\n'
                             'from . import views\n\n\n'
                             f"app_name = '{app_name}'\n\n"
                             'urlpatterns = [\n'
                             f"    path('', views.{app_name}_starter, "
                             f"name='{app_name}_all')\n"
                             ']')

        with open(os.path.join(app_name, 'urls.py'), 'w') as file:
            file.write(urls_file_content)

    @staticmethod
    def handle_settings(project_name, app_name):
        setting_path = os.path.join(project_name, 'settings.py')
        with open(setting_path) as file:
            content = file.read()
            pattern = re.compile("'django.contrib.staticfiles',\n", re.DOTALL)
            new_string = ("'django.contrib.staticfiles',\n\n"
                          '    # aditional packages:\n'
                          "    'django_extensions',\n\n"
                          '    # personal apps:\n"')
            new_string += f"'{app_name}', \n"
            content = pattern.sub(new_string, content)
            # print('content', content)
        with open(setting_path, 'w') as file:
            file.write(content)
