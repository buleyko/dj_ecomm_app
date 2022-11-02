class Repeater:
    def __init__(self):
        self.value = [1,2,3,4,5]
    def __iter__(self):
        print('q-q-q-q-q-q')
        for q in self.value:
            yield q 
    # def __next__(self):
    #     return self.value

print('--------')

for q in Repeater():
    print(q)


class Repeater2:
    def __init__(self):
        self._cursor = 0
        self._value = [1,2,3,4,5,6,7,8,9]
    def __iter__(self):
        print('=-=-=-=-=')
        return self
    def __next__(self):
        if self._cursor >= len(self._value):
            raise StopIteration 
        value = self._value[self._cursor]
        self._cursor += 1
        return value

# from decimal import Decimal
# from django.utils.translation import get_language
# from ecomm.apps.fnd.models import (
# 	Product, 
# 	ProductBaseTranslation,
# )



# class Comparison():
# 	def __init__(self, request):
# 		self.session = request.session
# 		compare = self.session.get('compare')
# 		compare_prod_ids = request.user.get_comparison() if request.user.is_authenticated else []
# 		if 'compare' not in request.session:
# 			compare = self.session['compare'] = {str(i):{'id':i} for i in compare_prod_ids}
# 		self.compare = compare

# 	def __iter__(self):
# 		product_ids = self.compare.keys()
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
# 			self.compare[str(prod['id'])]['product'] = prod

# 		compare = self.compare.copy()

# 		for item in compare.values():
# 			yield item

# 	def __len__(self):
# 		return len(self.compare)

# 	def get_product_ids(self):
# 		return [int(k) for k in self.compare.keys()]

# 	def add(self, product_id):
# 		self.compare[str(product_id)] = {'id':product_id}
# 		self.save()

# 	def delete(self, product_id):
# 		product_id = str(product_id)
# 		if product_id in self.compare:
# 			del self.compare[product_id]
# 			self.save()

# 	def clear(self):
# 		del self.session['compare']
# 		self.save()
		
# 	def save(self):
# 		self.session.modified = True
