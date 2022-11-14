import random
from django.core.management.base import BaseCommand, CommandError
from django_seed import Seed
from django.conf import settings
from ecomm.apps.fnd.models import (
	Fnd,
	Category,
	Brand,
	Delivery,
	ProductBase,
	Product,
	ProductAttribute,
	ProductAttributeValue,
	ProductType,
	ProductTypeAttribute,
	SaleType,
	Coupon,
	Sale,
)
from django.contrib.auth import get_user_model
Account = get_user_model()

seeder = Seed.seeder()

class Command(BaseCommand):
	help = 'Insert data to database'

	# any_seed_data = ['1', '2', '3']
	# 'field': lambda x: any_seed_data(randint(0, len(any_seed_data)))

	# name_postfixes = ['One', 'Two', 'Three', 'Four', 'Five']

	def handle(self, *args, **options):
		pass
		# try:
		# 	account = Account.objs.first()
		# 	fnd = Fnd.objs.get(alias=settings.FND_ALIAS)

		# 	try:
		# 		for index, name_postfix in enumerate(self.name_postfixes):
		# 			cat = Category.objs.create(
		# 				slug = f'cat-{name_postfix}-{seeder.faker.pystr(max_chars=8)}',
		# 				name = {'title':f'Category-{index}'},
		# 				parent = None,
		# 				is_shown = True,
		# 				created_by = account,
		# 				fnd = fnd,
		# 			)
		# 			for index, name_postfix in enumerate(self.name_postfixes):
		# 				child_cat = Category.objs.create(
		# 					slug = f'cat-{cat.id}-{seeder.faker.pystr(max_chars=8)}',
		# 					name = {'title':f'Category-{cat.id}-{index}'},
		# 					parent = cat,
		# 					is_shown = True,
		# 					created_by = account,
		# 					fnd = fnd,
		# 				)
		# 		self.stdout.write(self.style.SUCCESS('Added Categories'))
		# 	except:
		# 		self.stdout.write(self.style.ERROR('ERROR add categories'))

		# 	try:
		# 		seeder.add_entity(Brand, 20, {
		# 			'slug': lambda x: seeder.faker.pystr(max_chars=8),
		# 			'name': {"title":"Brand"},
		# 			'created_by': account,
		# 			'fnd': fnd,
		# 		})
		# 		seeder.execute()
		# 		self.stdout.write(self.style.SUCCESS('Added Brands'))
		# 	except:
		# 		self.stdout.write(self.style.ERROR('ERROR add brands'))

		# 	try:
		# 		seeder.add_entity(Delivery, 5, {
		# 			'name': {"title":"Delivary"},
		# 			'price': lambda x: random.randint(10, 50),
		# 			'method': 'HD',
		# 			'time_frame': '2-3',
		# 			'time_window': '15-18',
		# 			'position': 0,
		# 			'fnd': fnd,
		# 		})
		# 		seeder.execute()
		# 		self.stdout.write(self.style.SUCCESS('Added delivaries'))
		# 	except:
		# 		self.stdout.write(self.style.ERROR('ERROR add deliveries'))

		# 	try:
		# 		seeder.add_entity(ProductAttribute, 10, {
		# 			'slug': lambda x: seeder.faker.pystr(max_chars=8),
		# 			'name': {"title":"Attr"},
		# 			'fnd': fnd,
		# 		})
		# 		seeder.execute()
		# 		self.stdout.write(self.style.SUCCESS('Added attributes'))
		# 	except:
		# 		self.stdout.write(self.style.ERROR('ERROR add attributes'))

		# 	try:
		# 		attributes = ProductAttribute.objs.all()
		# 		for attr in attributes:
		# 			seeder.add_entity(ProductAttributeValue, 5, {
		# 				'product_attribute': attr,
		# 				'value': 'value',
		# 				'trs': {'title': 'Value'},
		# 			})
		# 			seeder.execute()
		# 		self.stdout.write(self.style.SUCCESS('Added attribute values'))
		# 	except:
		# 		self.stdout.write(self.style.ERROR('ERROR add attribute values'))

		# 	try:
		# 		categoryes = Category.objs.all()
		# 		attrs = list(ProductAttribute.objs.all())
		# 		for cat in categoryes:
		# 			for _ in range(1, 6):
		# 				prod_type = ProductType.objs.create(**{
		# 					'slug': seeder.faker.pystr(max_chars=8),
		# 					'name': {"title":"Type"},
		# 					'category': cat,
		# 					'in_menu': True,
		# 					'fnd': fnd,
		# 				})
		# 				prod_type.product_type_attributes.add(random.choice(attrs))
		# 				prod_type.save()
		# 		self.stdout.write(self.style.SUCCESS('Added product types'))
		# 	except:
		# 		self.stdout.write(self.style.ERROR('ERROR add product types'))

		# 	try:
		# 		categoryes = Category.objs.all()
		# 		for cat in categoryes:
		# 			seeder.add_entity(ProductBase, 25, {
		# 				'slug': lambda x: seeder.faker.pystr(max_chars=8),
		# 				'name': {'title': seeder.faker.bothify(text='Product????', letters='ABCDE')}, 
		# 				'short_desc': 'Short description',
		# 				'category': cat,
		# 				'created_by': account,
		# 				'fnd': fnd,
		# 			})
		# 			seeder.execute()
		# 		self.stdout.write(self.style.SUCCESS('Added base products'))
		# 	except:
		# 		self.stdout.write(self.style.ERROR('ERROR add base products'))

		# 	try:
		# 		base_products = ProductBase.objs.all()
		# 		brands = list(Brand.objs.all())
		# 		prod_types = list(ProductType.objs.all())
		# 		attr_vals = list(ProductAttributeValue.objs.all())
		# 		for base_prod in base_products:
		# 			prod = Product.objs.create(**{
		# 				'slug': seeder.faker.pystr(max_chars=8),
		# 				'sku': seeder.faker.pystr(max_chars=8),
		# 				'prod_base': base_prod,
		# 				'brand': random.choice(brands),
		# 				'product_type': random.choice(prod_types),
		# 				'is_default': True,
		# 				'price': random.randint(15, 100),
		# 				'created_by': account,
		# 				'fnd': fnd,
		# 			})
		# 			vals = [
		# 				random.choice(attr_vals),
		# 				random.choice(attr_vals),
		# 			]
		# 			prod.attribute_values.add(*vals)
		# 			prod.save()
		# 		self.stdout.write(self.style.SUCCESS('Added products'))
		# 	except:
		# 		self.stdout.write(self.style.ERROR('ERROR add products'))

		# except:
		# 	raise CommandError('ERROR add data (superuser of foundation not exist)')

		# self.stdout.write(self.style.SUCCESS('Successfully add data'))

