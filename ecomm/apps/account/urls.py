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

	path('address/list/', address.index, name='address_list'),
	path('address/create/', address.create, name='address_create'),
	path('address/store/', address.store, name='address_store'),
	path('address/edit/', address.edit, name='address_edit'),
	path('address/update/', address.update, name='address_update'),
	path('address/destroy/', address.destroy, name='address_destroy'),
	path('address/set-default', address.set_default, name='address_set_default'),

	path('reset-passwd/create', reset.reset_passwd_create, name='reset_passwd_create'),
	path('reset-passwd/mail', reset.reset_passwd_mail, name='reset_passwd_mail'),
	path('confirm-passwd/create', reset.confirm_passwd_create, name='confirm_passwd_create'),
	path('confirm-passwd/store', reset.confirm_passwd_store, name='confirm_passwd_store'),
	path('confirm-passwd/from-mail/<slug:uidb64>/<slug:token>/', reset.confirm_passwd_from_mail, name='confirm_passwd_from_mail'),
]