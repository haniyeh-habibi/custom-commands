from django.core.management.base import BaseCommand, CommandError
from Issues.models import Issues


class Command(BaseCommand):
    help = 'Closes the specified issue'

    def add_arguments(self, parser):
        parser.add_argument('issue_ids', nargs='+', type=int)

        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete poll instead of closing it',
        )

    def handle(self, *args, **options):
        for issue_id in options['issue_ids']:
            try:
                issue = Issues.objects.get(pk=issue_id)
            except Issues.DoesNotExist:
                raise CommandError(f'Issue {issue_id} does not exist')

            if options['delete']:
                issue.delete()
                self.stdout.write(self.style.SUCCESS(f'Successfully deleted Issue {issue_id}'))
            elif issue.is_open:
                issue.is_open = False
                self.stdout.write(self.style.SUCCESS(f'Successfully closed Issue {issue_id}'))
            else:
                self.stdout.write(self.style.SUCCESS('Issue is not open!'))
            issue.save()
