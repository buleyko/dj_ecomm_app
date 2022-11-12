from django.urls import path, include
from ecomm.apps.account.views import (
	address,
	dashboard,
	orders,
	reset,
	auth,
)


app_name = 'account'

urlpatterns = [
	path('dashboard/', dashboard.index, name='dashboard'),
	path('orders/', orders.index, name='orders'),

	path('signin/', auth.signin, name='signin'),
	path('entry/', auth.entry, name='entry'),
	path('signup/', auth.signup, name='signup'),
	path('registration/', auth.registration, name='registration'),
	path('signout/', auth.signout, name='signout'),
	path('activate/<slug:uidb64>/<slug:token>/', auth.account_activate, name='activate'),

	path('address/', include([
        path('list/', address.index, name='address_list'),
		# path('create/', address.create, name='address_create'),
		# path('store/', address.store, name='address_store'),
		path('edit/<int:pk>/', address.edit, name='address_edit'),
		path('update/', address.update, name='address_update'),
		path('destroy/<int:pk>/', address.destroy, name='address_destroy'),
		path('set-default/<int:pk>/', address.set_default, name='address_set_default'),
    ])),

	path('reset-passwd/', include([
		path('create', reset.reset_passwd_create, name='reset_passwd_create'),
		path('mail', reset.reset_passwd_mail, name='reset_passwd_mail'),
	])),

	path('confirm-passwd/', include([
		path('create', reset.confirm_passwd_create, name='confirm_passwd_create'),
		path('store', reset.confirm_passwd_store, name='confirm_passwd_store'),
		path('from-mail/<slug:uidb64>/<slug:token>/', reset.confirm_passwd_from_mail, name='confirm_passwd_from_mail'),
	])),
]