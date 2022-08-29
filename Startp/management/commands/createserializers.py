import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = ''

    # TODO add rest_framwork to settings
    def handle(self, *args, **options):
        app_name = options.pop('app_name')
        # target = options.pop('directory')
        os.chdir(f'{app_name}')
        model = 'Account'
        with open('serializers.py', 'w') as file:
            serializer_file_content = (
                'from rest_framework import serializers\n'
                f'from models import {model}\n\n\n'
                f'class {model}Serializer(serializers.ModelSerializer):\n'
                '    class Meta:\n'
                f'        model = {model}\n'
            )
            file.write(serializer_file_content)
        self.handle_views(model)

    def add_arguments(self, parser):
        parser.add_argument('app_name')
        parser.add_argument(
            '--app',
            dest='app_name',
            action='store_true',
        )

    @staticmethod
    def handle_views(model):
        with open('views.py', 'w') as file:
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
            file.write(views)
