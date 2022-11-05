from django.core.management.base import BaseCommand, CommandError
from ecomm.apps.fnd.models import Fnd

class Command(BaseCommand):
    help = 'Create Foundation with alias'

    def add_arguments(self, parser):
        parser.add_argument('alias', type=str)

    def handle(self, *args, **options):
        if options.get('alias', False):
            alias = options['alias']
            fnd = Fnd.objs.filter(alias=alias).first()
            if fnd is not None:
                raise CommandError(f'Foundation with alias:{alias} does exist')

            try:
                fnd = Fnd.objs.create(alias=alias, is_shown=True)
                fnd.save()
            except:
                raise CommandError('ERROR Foundation creation')

            self.stdout.write(self.style.SUCCESS(f'Successfully created fpoundation with alias: {alias}'))