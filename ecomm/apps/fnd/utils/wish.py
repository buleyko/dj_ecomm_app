# from decimal import Decimal
# from django.utils.translation import get_language
# from django.db.models import Prefetch
# from ecomm.apps.fnd.models import (
# 	Product, 
# 	ProductBaseTranslation,
# )



# class Wish():
# 	def __init__(self, request):
# 		self.session = request.session
# 		wish = self.session.get('wish')
# 		wish_prod_ids = request.user.get_wish() if request.user.is_authenticated else []
# 		if 'wish' not in request.session:
# 			wish = self.session['wish'] = {str(i):{'id':i} for i in wish_prod_ids}
# 		self.wish = wish

# 	def __iter__(self):
# 		product_ids = self.wish.keys()
# 		products = Product.objs.fnd().valid().shown().\
# 			filter(id__in=product_ids).values(
# 				'id', 'prod_base_id', 'prod_base__title', 'thumb', 'ext_name', 'price', 'sale_price',
# 			)
# 		base_prod_ids = [prod['prod_base_id'] for prod in products]
# 		translations = ProductBaseTranslation.objs.\
# 			filter(prod_base_id__in=base_prod_ids).\
# 			filter(lang_id=get_language()).values(
# 				'name', 'short_desc', 'prod_base_id',
# 			)
# 		for prod in products:
# 			prod['tr'] = {key: val for tr in translations for key, val in tr.items() if tr['prod_base_id'] == prod['prod_base_id']}
# 			self.wish[str(prod['id'])]['product'] = prod

# 		wish = self.wish.copy()

# 		for item in wish.values():
# 			yield item

# 	def __len__(self):
# 		return len(self.wish)

# 	def get_product_ids(self):
# 		return [int(k) for k in self.wish.keys()]

# 	def add(self, product_id):
# 		self.wish[str(product_id)] = {'id':product_id}
# 		self.save()

# 	def delete(self, product_id):
# 		product_id = str(product_id)
# 		if product_id in self.wish:
# 			del self.wish[product_id]
# 			self.save()

# 	def clear(self):
# 		del self.session['wish']
# 		self.save()
		
# 	def save(self):
# 		self.session.modified = True
