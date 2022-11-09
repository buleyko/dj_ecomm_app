from django.urls import path, include
from ecomm.apps.fnd.views import (
    fnd,
    cart,
    checkout,
    wish,
    comparison,
    category,
    product,
)

app_name = 'fnd'

urlpatterns = [
    path('', fnd.home, name='home'),
    path('options/', fnd.options, name='options'),
    path('change-language/<str:lang>/', fnd.change_language, name='change_language'),

    path('category/<slug:cat_slug>/', category.show, name='category'),
    path('product/<slug:prod_slug>/', product.show, name='product'),

    path('wish/', include([
        path('', wish.index, name='wish'),
        path('add/', wish.add, name='wish_add'),
        path('delete/', wish.delete, name='wish_delete'),
        path('remove-from-list/<slug:prod_slug>/', wish.remove, name='wish_remove_from_list'),
    ])),

    path('comparison/', include([
        path('', comparison.index, name='comparison'),
        path('add/', comparison.add, name='comparison_add'),
        path('delete/', comparison.delete, name='comparison_delete'),
        path('remove-from-list/<slug:prod_slug>/', comparison.remove, name='comparison_remove_from_list'),
    ])),

    path('cart/', include([
        path('', cart.index, name='cart'),
        path('add/', cart.add, name='cart_add'),
        path('update/', cart.update, name='cart_update'),
        path('delete/', cart.delete, name='cart_delete'),
    ])),

    path('checkout/', include([
        path('', checkout.index, name='checkout'),
        path('update-delivery/', checkout.update_delivery, name='checkout_update_delivery'),
        path('payment-complete/', checkout.payment_complete, name='checkout_payment_complete'),
        path('payment-successful/', checkout.payment_successful, name='checkout_payment_successful'),
    ])),
]