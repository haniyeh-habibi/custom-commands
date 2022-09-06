import os
import re

from django.core.management.commands import startproject


class Command(startproject.Command):
    help = 'Creates a Django project with additional features'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

        parser.add_argument('app')
        parser.add_argument('settings')

        parser.add_argument(
            '--app',
            dest='app_name',
            action='store_true',
            help='Name of the application',
        )
        parser.add_argument(
            '--setting',
            dest='settings',
            action='store_true',
            help='if t: Change settings'
        )

    def handle(self, *args, **options):
        project_name = options.get('name')
        super(Command, self).handle(**options)
        os.chdir(project_name)
        self.create_venv()
        app_name = options.get('app')
        if app_name:
            self.create_apps(app_name, project_name)
            if options.get('settings') == 't':
                self.handle_settings(project_name, app_name)

    @staticmethod
    def create_venv():
        """
        creates a virtual environment with venv
        """
        os.system(f'python3 -m venv env')
        print(f'Created virtual environment: env')

    def create_apps(self, app_name, project_name):
        """
        creates app named in argument --app
        """
        os.system(f'python manage.py startapp {app_name}')

        # creates templates folder structure
        os.makedirs(os.path.join(app_name, 'templates'), exist_ok=True)
        os.makedirs(os.path.join(app_name, 'templates', app_name), exist_ok=True)
        self.modify_views_py(app_name)
        self.create_urls_py(app_name)
        self.add_urls(app_name, project_name)
        self.create_extra_folders()

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
            print('created app urls.')

    @staticmethod
    def add_urls(app_name, project_name):
        """
        Add app urls to project urls

        Parameter:
        - app_name(str): the django app name.
        - project_name(str): the django project_name
        """

        urls_py_path = os.path.join(project_name, 'urls.py')
        with open(urls_py_path) as file:
            content = file.read()

            pattern = re.compile(r'\"\"\".*?\"\"\"\n{1,5}', re.DOTALL)
            content = pattern.sub('', content)

            # import include() function and add a temporary view function
            pattern = re.compile('import path\n', re.DOTALL)
            new = ('import path, include\n'
                   'from django.http import HttpResponse'
                   ' # remove this import later\n\n\n'
                   '# remove this function later:\n'
                   'def starter_home(request):\n'
                   '    return HttpResponse("<h1>HOME PAGE</h1>")\n\n')
            content = pattern.sub(new, content)

            # insert path to home page with the temporary function view we created
            pattern = re.compile(r'\[\n    ', re.DOTALL)
            new = r"[\n    path('', starter_home, name='home'),\n    "
            content = pattern.sub(new, content)

            new = f"    path('{app_name}/', include('{app_name}.urls')),\n"
            content = content.replace(']', new + ']')
        with open(urls_py_path, 'w') as file:
            file.write(content)
            print('added app urls to project urls.')

    @staticmethod
    def create_extra_folders():
        extra_folders = ['templates',
                         os.path.join('templates', 'static'),
                         'media',
                         'scripts']

        for folder in extra_folders:
            os.makedirs(folder, exist_ok=True)
        print('Created extra folders')

    @staticmethod
    def handle_settings(project_name, app_name):
        setting_path = os.path.join(project_name, 'settings.py')
        with open(setting_path) as file:
            content = file.read()

            # insert an import to the 'os' module
            pattern = re.compile('from pathlib import Path\n', re.DOTALL)
            content = pattern.sub('from pathlib import Path\nimport os\n\n', content)

            # insert django_extensions in INSTALLED_APPS
            pattern = re.compile('"django.contrib.staticfiles",', re.DOTALL)

            new_string = ('"django.contrib.staticfiles",\n'
                          f'    "{app_name}"')
            content = pattern.sub(new_string, content)

            # insert templates DIR info
            pattern = re.compile(r'"DIRS": \[\],', re.DOTALL)
            new = r'"DIRS": [os.path.join(BASE_DIR, "templates")],'
            content = pattern.sub(new, content)

            # change static info and add media info
            new = ("STATIC_URL = '/static/'\n"
                   "STATICFILES_DIRS = (os.path.join(BASE_DIR, 'templates', 'static'),)\n"
                   "STATIC_ROOT = os.path.join('static')\n\n"
                   "MEDIA_ROOT = os.path.join(BASE_DIR, 'media')\n"
                   "MEDIA_URL = '/media/'\n"
                   )
            pattern = re.compile('STATIC_URL = "static/"\n', re.DOTALL)
            content = pattern.sub(new, content)

        with open(setting_path, 'w') as file:
            file.write(content)
        print(f'Updated {project_name}/settings.py file')
