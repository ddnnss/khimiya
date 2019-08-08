from .models import Cart, Guest

def format_number(num):
    if num % 1 == 0:
        return int(num)
    else:
        return num

def items_in_cart(request):
    if request.user.is_authenticated:
        all_items_in_cart = Cart.objects.filter(client_id=request.user.id)
        used_promo = request.user.used_promo
        if not used_promo:
            promo_discount_value = 0
        print('Cart items for auth user')
        count_items_in_cart = all_items_in_cart.count()
        total_cart_price = 0
        for item in all_items_in_cart:
            total_cart_price += item.total_price
        print(total_cart_price)
        total_cart_price_with_discount = total_cart_price
        if used_promo:
            print('auth user with promo')
            promo_discount_value = used_promo.promo_discount
            total_cart_price_with_discount = format_number(total_cart_price - (total_cart_price * promo_discount_value / 100))

    else:
        s_key = request.session.session_key
        try:
            guest = Guest.objects.get(session=s_key)
            used_promo = guest.used_promo
            if not used_promo:
                promo_discount_value = 0

        except:
            guest = None
            used_promo = None
        if guest:
            all_items_in_cart = Cart.objects.filter(guest=guest)
            print('Cart items for NOT auth user')
            count_items_in_cart = all_items_in_cart.count()
            total_cart_price = 0

            for item in all_items_in_cart:
                total_cart_price += item.total_price
            total_cart_price_with_discount = total_cart_price
            print(total_cart_price)
            if used_promo:
                print('guest with promo')
                promo_discount_value = used_promo.promo_discount
                total_cart_price_with_discount = format_number(total_cart_price - (total_cart_price * promo_discount_value / 100))

    return locals()