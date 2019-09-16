import decimal

from django.shortcuts import render
from django.http import JsonResponse
from cart.models import Cart
from customuser.models import Guest
from item.models import PromoCode,Item,SubCategory
from datetime import datetime
from order.models import Wishlist


def format_number(num):
    if num % 1 == 0:
        return int(num)
    else:
        return num

def show_cart(request):

    return render(request, 'page/cart.html', locals())

def wishlist_delete(request):
    return_dict = {}
    if request.user.is_authenticated:
        Wishlist.objects.get(id=int(request.POST.get('id'))).delete()

        return_dict['result'] = True
    else:
        return_dict['result'] = False
    return JsonResponse(return_dict)

def wishlist_add(request):
    return_dict = {}
    if request.user.is_authenticated:
        Wishlist.objects.create(client=request.user, item_id=int(request.POST.get('item_id')))

        return_dict['result'] = True
    else:
        return_dict['result'] = False
    return JsonResponse(return_dict)

def add_to_cart(request):
    return_dict = {}

    data = request.POST
    print(data)
    s_key = request.session.session_key
    item_id = int(data.get('item_id'))
    item_number = int(data.get('item_number'))
    item_volume = decimal.Decimal(data.get('item_volume'))
    if request.user.is_authenticated:
        print('User is_authenticated')
        addtocart, created = Cart.objects.get_or_create(client=request.user,
                                                        item_id=item_id, defaults={'number': item_number})


        if not created:
            addtocart.number += int(item_number)
            addtocart.save(force_update=True)
        all_items_in_cart = Cart.objects.filter(client=request.user)

    else:
        print('User is_not authenticated')
        try:
            guest = Guest.objects.get(session=s_key)
            print('Guest already created')
        except:
            guest = None

        if not guest:
            guest = Guest.objects.create(session=s_key)
            guest.save()
            print('Guest created')

        addtocart, created = Cart.objects.get_or_create(guest=guest,
                                                           item_id=item_id, defaults={'number': item_number})
        if not created:
            addtocart.number += int(item_number)
            addtocart.save(force_update=True)

        all_items_in_cart = Cart.objects.filter(guest=guest)
    count_items_in_cart = all_items_in_cart.count()
    total_cart_price = 0

    return_dict['total_items_in_cart'] = count_items_in_cart
    return_dict['all_items'] = list()
    for item in all_items_in_cart:
        total_cart_price += item.total_price
        item_dict = dict()
        item_dict['id'] = item.id
        item_dict['name'] = item.item.item.name
        item_dict['name_slug'] = item.item.item.name_slug
        item_dict['price'] = item.current_price
        item_dict['total_price'] = item.total_price
        item_dict['volume'] = item.item.volume
        item_dict['number'] = item.number
        item_dict['image'] = item.item.item.itemimage_set.first().image_small
        return_dict['all_items'].append(item_dict)

    return_dict['total_cart_price'] = total_cart_price

    return JsonResponse(return_dict)

def delete_from_cart(request):
    return_dict = {}
    data = request.POST
    s_key = request.session.session_key
    item_id = int(data.get('item_id'))

    if request.user.is_authenticated:
        print('User is_authenticated')
        Cart.objects.filter(client=request.user, id=item_id).delete()
        all_items_in_cart = Cart.objects.filter(client=request.user)

    else:
        print('User is_not authenticated')

        guest = Guest.objects.get(session=s_key)
        Cart.objects.filter(guest=guest, id=item_id).delete()
        all_items_in_cart = Cart.objects.filter(guest=guest)
    count_items_in_cart = all_items_in_cart.count()
    total_cart_price = 0

    return_dict['total_items_in_cart'] = count_items_in_cart
    return_dict['all_items'] = list()
    for item in all_items_in_cart:
        total_cart_price += item.total_price
        item_dict = dict()
        item_dict['id'] = item.id
        item_dict['name'] = item.item.item.name
        item_dict['name_slug'] = item.item.item.name_slug
        item_dict['price'] = item.current_price
        item_dict['total_price'] = item.total_price
        item_dict['volume'] = item.item.volume
        item_dict['number'] = item.number
        item_dict['image'] = item.item.item.itemimage_set.first().image_small
        return_dict['all_items'].append(item_dict)

    return_dict['total_cart_price'] = total_cart_price
    return JsonResponse(return_dict)



def update_cart(request):
    return_dict = {}

    data = request.POST
    print(data)
    item_id = int(data.get('item_id'))
    item_number = int(data.get('item_number'))

    item = Cart.objects.get(id=item_id)
    item.number = item_number
    item.save(force_update=True)

    s_key = request.session.session_key

    if request.user.is_authenticated:
        print('update_cart : User is_authenticated')
        all_items_in_cart = Cart.objects.filter(client=request.user)
        used_promo = request.user.used_promo
        if not used_promo:
            promo_discount_value = 0

    else:
        print('update_cart : User is_not authenticated')

        guest = Guest.objects.get(session=s_key)
        all_items_in_cart = Cart.objects.filter(guest=guest)
        used_promo = guest.used_promo
        if not used_promo:
            promo_discount_value = 0

    count_items_in_cart = all_items_in_cart.count()
    total_cart_price = 0

    return_dict['total_items_in_cart'] = count_items_in_cart
    return_dict['all_items'] = list()
    for item in all_items_in_cart:
        total_cart_price += item.total_price
        item_dict = dict()
        item_dict['id'] = item.id
        item_dict['name'] = item.item.item.name
        item_dict['name_slug'] = item.item.item.name_slug
        item_dict['price'] = item.current_price
        item_dict['total_price'] = item.total_price
        item_dict['volume'] = item.item.volume
        item_dict['number'] = item.number
        item_dict['image'] = item.item.item.itemimage_set.first().image_small
        return_dict['all_items'].append(item_dict)
    total_cart_price_with_discount = total_cart_price
    if used_promo:
        print('with promo')
        promo_discount_value = used_promo.promo_discount
        total_cart_price_with_discount = format_number(
        total_cart_price - (total_cart_price * promo_discount_value / 100))


    return_dict['total_cart_price'] = total_cart_price
    return_dict['total_cart_price_with_discount'] = total_cart_price_with_discount
    return_dict['promo_discount_value'] = promo_discount_value

    return JsonResponse(return_dict)


def delete_from_main_cart(request):
    return_dict = {}

    data = request.POST
    print(data)
    item_id = int(data.get('item_id'))

    Cart.objects.get(id=item_id).delete()

    s_key = request.session.session_key

    if request.user.is_authenticated:
        print('delete_from_main_cart : User is_authenticated')
        all_items_in_cart = Cart.objects.filter(client=request.user)
        used_promo = request.user.used_promo
        if all_items_in_cart.count() == 0:
            request.user.used_promo = None
            promo_discount_value = 0
            used_promo = None
            request.user.save(force_update=True)
        if not used_promo:
            promo_discount_value = 0

    else:
        print('delete_from_main_cart : User is_not authenticated')

        guest = Guest.objects.get(session=s_key)
        all_items_in_cart = Cart.objects.filter(guest=guest)
        used_promo = guest.used_promo

        if all_items_in_cart.count() == 0:
            guest.used_promo = None
            promo_discount_value = 0
            used_promo = None
            guest.save(force_update=True)
        if not used_promo:
            promo_discount_value = 0
    count_items_in_cart = all_items_in_cart.count()
    total_cart_price = 0

    return_dict['total_items_in_cart'] = count_items_in_cart
    return_dict['all_items'] = list()
    for item in all_items_in_cart:
        total_cart_price += item.total_price
        item_dict = dict()
        item_dict['id'] = item.id
        item_dict['name'] = item.item.item.name
        item_dict['name_slug'] = item.item.item.name_slug
        item_dict['price'] = item.current_price
        item_dict['total_price'] = item.total_price
        item_dict['volume'] = item.item.volume
        item_dict['number'] = item.number
        item_dict['image'] = item.item.item.itemimage_set.first().image_small
        return_dict['all_items'].append(item_dict)

    return_dict['total_cart_price'] = total_cart_price
    total_cart_price_with_discount = total_cart_price
    if used_promo:
        print('with promo')
        promo_discount_value = used_promo.promo_discount
        total_cart_price_with_discount = format_number(
        total_cart_price - (total_cart_price * promo_discount_value / 100))

    return_dict['total_cart_price'] = total_cart_price
    return_dict['total_cart_price_with_discount'] = total_cart_price_with_discount
    return_dict['promo_discount_value'] = promo_discount_value

    return JsonResponse(return_dict)


def use_promo(request):
    return_dict = {}
    data = request.POST
    print(data)
    promo_code = data.get('promo_code')
    try:
        code = PromoCode.objects.get(promo_code=promo_code)
    except:
        code = None
    if code:
        print('code found')
        s_key = request.session.session_key

        if request.user.is_authenticated:
            print('use_promo : User is_authenticated')
            used_promo = request.user.used_promo

            guest = None
        else:
            print('use_promo : User is_not authenticated')
            guest = Guest.objects.get(session=s_key)
            used_promo = guest.used_promo

        if used_promo:
            print('use_promo : code used already')
            return_dict['result'] = False
        else:

            if code.is_unlimited:
                if code.expiry > datetime.now():
                    code_valid = True
                    print('valid unlim code')
                else:
                    code_valid = False
                    print('invalid unlim code')
            else:
                if code.use_counts > 0:
                    code_valid = True
                    code.use_counts -= 1
                    code.save(force_update=True)
                    print('valid lim code')
                else:
                    code_valid = False
                    print('invalid lim code')

            if not code_valid:
                return_dict['result'] = False
            else:

                if guest:
                    guest.used_promo = code
                    guest.save(force_update=True)
                    all_items_in_cart = Cart.objects.filter(guest=guest)

                else:
                    request.user.used_promo = code
                    request.user.save(force_update=True)
                    all_items_in_cart = Cart.objects.filter(client_id=request.user.id)

                total_cart_price = 0

                for item in all_items_in_cart:
                    total_cart_price += item.total_price

                promo_discount_value = code.promo_discount
                total_cart_price_with_discount = format_number(
                    total_cart_price - (total_cart_price * promo_discount_value / 100))

                return_dict['result'] = True
                return_dict['total_cart_price'] = total_cart_price
                return_dict['total_cart_price_with_discount'] = total_cart_price_with_discount
                return_dict['promo_discount_value'] = promo_discount_value


    else:
        print('code not found')
        return_dict['result'] = False
    return JsonResponse(return_dict)


def sort_filter(request):
    return_dict = {}
    data = request.GET
    print(data)
    search = data.get('search')
    filter = data.get('filter')
    order = data.get('order')
    subcat =data['subcat']
    sub = SubCategory.objects.get(id=subcat)
    if order:
        all_items = sub.item_set.all().order_by(order)
    else:
        all_items=sub.item_set.all()

    search_qs = None
    if search:
        search_qs = all_items.filter(name__contains=search)
        items = search_qs
        print(items)
    if filter:
        print('Поиск по фильтру')
        if search_qs:
            items = search_qs.filter(filter__name_slug=filter)
            print(items)
        else:
            items = all_items.filter(filter__name_slug=filter)
            print(items)

    return_dict['all_items'] = list()
    for item in items:
        item_dict = dict()
        item_dict['id'] = item.item.id
        item_dict['name'] = item.item.name
        item_dict['name_slug'] = item.item.name_slug
        item_dict['price'] = item.current_price
        item_dict['total_price'] = item.total_price
        item_dict['number'] = item.number
        item_dict['image'] = item.item.itemimage_set.first().image_small
        return_dict['all_items'].append(item_dict)


    return JsonResponse(return_dict)