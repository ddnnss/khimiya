import json

from django import template

register = template.Library()

@register.filter
def check_discount(data):
    returnString = ''
    for price in data.itemprice_set.all():
        if price.discount > 0:
            return f'<p>{price.volume} {price.unit} - <del>{price.price}</del> {price.price_with_discount} РУБ</p>'
        else:
            returnString = f'<p>{price.volume} {price.unit} - {price.price} РУБ</p>'
    return returnString


@register.filter
def is_discount(data):
    returnString = ''
    for price in data.itemprice_set.all():
        if price.discount > 0:
            return f'<div class="item-card-discount">- {price.discount}%</div>'
        else:
            returnString = ''
    return returnString


