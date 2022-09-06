import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates serializers from models'

    def add_arguments(self, parser):
        parser.add_argument('app_name')
        parser.add_argument('model')

        parser.add_argument(
            '--app',
            dest='app_name',
            action='store_true',
        )
        parser.add_argument(
            '--model',
            dest='model',
            action='store_true'
        )

    def handle(self, *args, **options):
        app_name = options.get('app_name')
        model = options.get('model')
        if not os.path.isdir(app_name):
            print(f'App {app_name} does not exist.')
            return
        os.chdir(f'{app_name}')
        print('Installing djangorestframework package from pip')
        os.system('pip install djangorestframework')
        print('Installed djangorestframework.')
        with open('serializers.py'):
            serializer_file_content = (
                'from rest_framework import serializers\n'
                f'from models import {model}\n\n\n'
                f'class {model}Serializer(serializers.ModelSerializer):\n'
                '    class Meta:\n'
                f'        model = {model}\n'
            )
        with open('serializers.py', 'w') as file:
            file.write(serializer_file_content)
            print('Created model serializers.')
        self.handle_views(model)

    @staticmethod
    def handle_views(model):
        with open('views.py'):
            views = (
                'from rest_framework import viewsets\n'
                f'from serializers import {model}Serializer\n\n\n'
                'class GeneralViewSet(viewsets.ModelViewSet):\n'
                '    def get_queryset(self):\n'
                "        model = self.kwargs.get('model')\n"
                '        return model.objects.all()\n\n'

                '    def get_serializer_class(self):\n'
                f"        {model}Serializer.Meta.model = self.kwargs.get('model')\n"
                f'        return {model}Serializer\n'
            )
        with open('views.py', 'w') as file:
            file.write(views)
            print('Created Views.')
