from django.shortcuts import render
from django.http import JsonResponse, Http404
from item.models import Item,ItemImage
from cart.models import Cart
from customuser.models import User, Guest

def quick_view(request):
    return_dict = {}
    data = request.POST
    print(data)
    item_id = int(data.get('item_id'))
    item = Item.objects.get(id=item_id)
    images = ItemImage.objects.filter(item_id=item_id)
    if item.discount > 0:
        return_dict['item_price_discount'] = item.discount_value
    return_dict['item_id'] = item.id
    return_dict['item_name'] = item.name
    return_dict['item_name_slug'] = item.name_slug
    return_dict['item_description'] = item.description
    return_dict['item_price'] = item.price
    return_dict['item_discount'] = item.discount
    return_dict['item_new'] = item.is_new
    return_dict['item_article'] = item.article
    return_dict['item_present'] = item.is_present
    return_dict['item_images'] = list()
    for image in images:
        return_dict['item_images'].append(image.image_small)
    return JsonResponse(return_dict)




def item_page(request, item_slug):
    print(request.get_host())
    try:
        item = Item.objects.get(name_slug=item_slug)
        item.views += 1
        item.save(force_update=True)
        recomended = Item.objects.filter(subcategory_id=item.subcategory_id).order_by('-views')[:12]
        # title = item.name
        # description = item.description

        print(recomended)
    except:
        raise Http404
        # return render(request, '404.html', locals())
    title = '{} | артикул {} - купить оптом в Москве'.format(item.name, item.article)
    description = 'Заказывайте оптом {} (артикул {}) в интернет-магазине ЛАКШМИ.' \
                  ' Большой выбор товаров на различную тематику по доступным ценам. Доставка по России.'.format(item.name, item.article)
    return render(request, 'item/item.html', locals())