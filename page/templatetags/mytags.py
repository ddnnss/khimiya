import json

from django import template

register = template.Library()

@register.filter
def check_discount(data):
    returnString = ''
    withDiscount = False
    for price in data.itemprice_set.all():
        if price.discount > 0:
          withDiscount = True
          returnString = f'<p>{price.volume} {price.unit} - <del>{price.price}</del> {price.price_with_discount} РУБ</p>'
        else:
            pass
    if withDiscount:
        return returnString
    else:

        return f'<p>{data.itemprice_set.first().volume} {data.itemprice_set.first().unit} - {data.itemprice_set.first().price} РУБ</p>'


@register.filter
def is_discount(data):
    returnString = ''
    for price in data.itemprice_set.all():
        if price.discount > 0:
            return f'<div class="item-card-discount">- {price.discount}%</div>'
        else:
            returnString = ''
    return returnString


