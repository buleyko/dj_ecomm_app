from random import randint
from django.core.management.base import BaseCommand, CommandError
from django_seed import Seed
from django.conf import settings
from ecomm.apps.fnd.models import (
	Fnd,
	Category,
)
from django.contrib.auth import get_user_model
Account = get_user_model()

seeder = Seed.seeder()

class Command(BaseCommand):
	help = 'Insert data to database'

	# any_seed_data = ['1', '2', '3']
	# 'field': lambda x: any_seed_data(randint(0, len(any_seed_data)))

	def handle(self, *args, **options):
		try:
			account = Account.objs.get(id=1)
			fnd = Fnd.objs.get(alias=settings.FND_ALIAS)
			for i in [i for i in range(1, 6)]:
				seeder.add_entity(Category, 1, {
					'slug': f'cat-{i}',
					'name': {'title':f'Category-{i}'},
					'thumb': None,
					'parent': None,
					'created_by': account,
					'is_blocked': False,
					'is_shown': True,
					'lft': 1,
					'rght': 4,
					'tree_id': 1,
					'level': 0,
					'fnd': fnd,
					'created_at': seeder.faker.date_time(),
				})
			seeder.execute()
			self.stdout.write(self.style.SUCCESS('Added Categories'))

			# seeder.add_entity(Author, 50, {
			# 	'full_name': '{"en":"Qwerty Qwerty"}',
			# })

			# seeder.add_entity(ItemType, 20, {
			# 	'slug': lambda x: seeder.faker.pystr(max_chars=8),
			# 	'name': '{"en":"Qwerty"}',
			# 	'created_by': account,
			# 	'created_at': seeder.faker.date_time(),
			# })
			# seeder.execute()
			# self.stdout.write(self.style.SUCCESS('Added Types'))

			# category = Category.objs.get(id=1)
			# item_type = ItemType.objs.get(id=1)
			# seeder.add_entity(Item, 200, {
			# 	'slug': lambda x: seeder.faker.pystr(max_chars=8),
			# 	'title': 'CatTitle',
			# 	'name': '{"en":"Qwerty"}',
			# 	'published': seeder.faker.date_time(),
			# 	'publisher': 'Publisher',
			# 	'created_by': account,
			# 	'category': category,
			# 	'item_type': item_type,
			# })
			# seeder.execute()
			# self.stdout.write(self.style.SUCCESS('Add Items'))
		except:
			raise CommandError('ERROR add data')

		self.stdout.write(self.style.SUCCESS('Successfully add data'))

