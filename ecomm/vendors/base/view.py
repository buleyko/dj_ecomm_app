# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from django.views.generic.base import ContextMixin
# from ecomm.vendors.mixins.view import CommonContextMixin
# from django.shortcuts import render
# from django.http import Http404
# from django.views import View
# from django.core.exceptions import PermissionDenied
# from django.http import ( 
# 	JsonResponse, 
# 	HttpResponse, 
# )


# class BaseView(CommonContextMixin, ContextMixin, View):
# 	""" Base View class for all view """
# 	template_name = ''
# 	context = {}
# 	title = None

# 	# def setup(self, *args, **kwargs):
# 	# 	return super().setup(*args, **kwargs)
 	
# 	def dispatch(self, *args, **kwargs):
# 		return super().dispatch(*args, **kwargs)

# 	def render_out(self, request):
# 		""" 
# 		Render and return page with data 
# 		from context:dict and common_context:dict
# 		"""
# 		self.context['title'] = self.title
# 		self.context.update(self.get_common_context_data())
# 		return render(request, self.template_name, self.context)

# 	def json_out(self):
# 		""" Return JSON from context:dict """
# 		return JsonResponse(self.context)


# class View(BaseView):
# 	""" Base View for all open pages """
# 	pass 

# class AdminView(BaseView):
# 	""" Base View for all closed pages """

# 	@method_decorator([login_required])
# 	def dispatch(self, *args, **kwargs):
# 		return super().dispatch(*args, **kwargs)