from django import template

register = template.Library()

@register.simple_tag
def cart_product_qty(cart, item_id):
    return cart.get_product_quantity(item_id)