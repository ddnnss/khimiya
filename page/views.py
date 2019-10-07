from django.shortcuts import render, render_to_response
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .models import Banner
from item.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from customuser.forms import SignUpForm, UpdateForm
from order.models import *
from cart.models import Cart
from customuser.models import User, Guest
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import Http404



def create_password():
    from random import choices
    import string
    password = ''.join(choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))
    return password

def is_email(string):

    from django.core.exceptions import ValidationError
    from django.core.validators import EmailValidator

    validator = EmailValidator()
    try:
        validator(string)
    except ValidationError:
        return False

    return True

def showitem(request, cat_slug,subcat_slug,subsubcat_slug,item_slug):
    try:
        item = Item.objects.get(name_slug=item_slug)
        item.views += 1
        item.save(force_update=True)
        cat = Category.objects.get(name_slug=cat_slug)
        images = ItemImage.objects.filter(item=item)
        # cat.views += 1
        # cat.save()
        volumes = item.itemprice_set.all()
        title = 'Купить {} в - интернет-магазин САЙТ'.format(item.name)
        description = 'В нашем интернет магазине Вы можете купить {} в ГОРОДЕ с бесплатной доставкой.'.format(item.name)
        keywords = '{} купить, {} цена, {} интернет магазин, {} доставка'.format(item.name,item.name,item.name,item.name)
        subcat = SubCategory.objects.get(name_slug=subcat_slug)
        subsubcat = SubSubCategory.objects.get(name_slug=subsubcat_slug)
       # recomended = Item.objects.filter(subcategory_id=item.subcategory_id).order_by('-views')[:12]
        print(request.META['HTTP_HOST'])
        return render(request, 'page/item.html', locals())
    except:
       raise Http404
        # return render(request, '404.html', locals())



def check_email(request):
    return_dict = {}
    email = request.POST.get('email')
    print(email)
    email_error = ''
    if is_email(email):
        email_is_valid = True
    else:
        email_is_valid = False
        email_error = 'Указанный адрес почты не верный'

    try:
        user = User.objects.get(email=email)
    except:
        user = None

    if user:
        email_is_valid = False
        email_error = 'Указанный адрес почты уже зарегистрирован'

    return_dict['result'] = email_is_valid
    return_dict['email_error'] = email_error
    return JsonResponse(return_dict)


def order(request, order_code):
    try:
        order = Order.objects.get(order_code=order_code)
    except:
        order=None

    if order:
        return render(request, 'page/order.html', locals())
    else:
        raise Http404
        # return render(request, '404.html', locals())

def about_us(request):
    title = 'О НАС'
    show_tags = True
    # if request.GET.get('sendmail') == '1':
    #     users = User.objects.all()
    #     for user in users:
    #         msg_html = render_to_string('email/sendmail.html')
    #         send_mail('Акция: 10% на фен шуй товары до 30.04', None, 'info@lakshmi888.ru', [user.email],
    #               fail_silently=False, html_message=msg_html)
    return render(request, 'page/about_us.html', locals())


def robots(request):

    return render(request, 'page/robots.txt')

def sitemap(request):
    return render(request, 'page/sitemap.xml', content_type = "application/xhtml+xml")




def contacts(request):
    show_tags = True
    title = 'КОНТАКТНАЯ ИНФОРМАЦИЯ'
    return render(request, 'page/contacts.html', locals())


def dostavka(request):
    show_tags = True
    title = 'ИНФОРМАЦИЯ О ДОСТАВКЕ'
    return render(request, 'page/dostavka.html', locals())


def new(request):
    all_items = Item.objects.filter(is_new=True, is_active=True, is_present=True).order_by('-created_at')
    not_present = Item.objects.filter(is_new=True, is_active=True, is_present=False)
    data = request.GET
    print(request.GET)
    search = data.get('search')
    filter = data.get('filter')
    order = data.get('order')
    count = data.get('count')
    page = request.GET.get('page')
    search_qs = None
    filter_sq = None
    if search:
        items = all_items.filter(name_lower__contains=search.lower())
        if not items:
            items = all_items.filter(article__contains=search)
        search_qs = items

        param_search = search

    if filter == 'new':
        print('Поиск по фильтру туц')
        if search_qs:
            items = search_qs.filter(is_new=True)
            filter_sq = items
            param_filter = filter
        else:
            items = all_items.filter(is_new=True)
            filter_sq = items
            param_filter = filter

        param_filter = 'new'

    if filter and filter != 'new':
        print('Поиск по фильтру')

        if search_qs:
            items = search_qs.filter(filter__name_slug=filter)
            filter_sq = items
            param_filter = filter
        else:
            items = all_items.filter(filter__name_slug=filter)
            filter_sq = items
            param_filter = filter

    if order:
        if search_qs and filter_sq:
            items = filter_sq.order_by(order)
        elif filter_sq:
            items = filter_sq.order_by(order)
        elif search_qs:
            items = search_qs.order_by(order)
        else:
            items = all_items.order_by(order)
        param_order = order

    if not search and not order and not filter:
        items = all_items
        # subcat.views = subcat.views + 1
        # subcat.save()
        param_order = '-created_at'

    if count:
        items_paginator = Paginator(items, int(count))
        param_count = count
    else:
        items_paginator = Paginator(items, 12)

    if page:
        canonical_link = '/new/'

    try:
        items = items_paginator.get_page(page)
    except PageNotAnInteger:
        items = items_paginator.page(1)
    except EmptyPage:
        items = items_paginator.page(items_paginator.num_pages)
    show_tags = False
    return render(request, 'page/new.html', locals())




def checkout(request):
    show_tags = True
    if request.POST:
        if request.POST.get('form_type') == 'user_info':
            client = request.user
            mail_tmp = client.is_allow_email
            form = UpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                client.profile_ok = True
                client.is_allow_email = mail_tmp
                client.save(force_update=True)

                return HttpResponseRedirect('/checkout/')
            else:
                client = request.user
                form = UpdateForm(instance=client)
                return HttpResponseRedirect('/checkout/')

        if request.POST.get('form_type') == 'checkout':
            order_code = create_password()
            if request.user.used_promo:
                promo_id = request.user.used_promo.id
            else:
                promo_id = None
            order = Order.objects.create(client=request.user, promo_code_id=promo_id, order_code=order_code,
                                         payment_id=int(request.POST.get('payment')),
                                         shipping_id=int(request.POST.get('shipping')))
            order.save(force_update=True)
            all_cart_items = Cart.objects.filter(client_id=request.user.id)
            for item in all_cart_items:
                ItemsInOrder.objects.create(order_id=order.id, item_id=item.item.id, number=item.number)
                item.item.item.buys = item.item.item.buys + 1
                item.item.item.save(force_update=True)
            all_cart_items.delete()
            request.user.used_promo = None

            new_order = Order.objects.get(id=order.id)

            want_to_use_bonuse = int(request.POST.get('form_use_bonuses'))
            print('want_to_use_bonuse',want_to_use_bonuse)
            print('user avaialble bonese /2',request.user.bonuses / 2)
            print('request.user.bonuses1', request.user.bonuses)
            if want_to_use_bonuse > 0 and want_to_use_bonuse <= int(request.user.bonuses / 2):
                request.user.bonuses -= want_to_use_bonuse
                new_order.bonuses = want_to_use_bonuse
                request.user.save(force_update=True)
                print('request.user.bonuses2', request.user.bonuses)
            print('cart cost before',new_order.total_price_with_code)
            new_order.save(force_update=True)
            print('cart cost after', new_order.total_price_with_code)
            print('request.user.bonuses3', request.user.bonuses)
            request.user.bonuses += int(float(new_order.total_price_with_code) * (3/100))
            request.user.save(force_update=True)
            print('int(float(new_order.total_price_with_code) * (3/100))', int(float(new_order.total_price_with_code) * (3/100)))
            print('request.user.bonuses4', request.user.bonuses)



            # msg_html = render_to_string('email/new_order.html', {'order': new_order})
            # send_mail('Заказ успешно размещен', None, 'info@lakshmi888.ru', [request.user.email],
            #           fail_silently=False, html_message=msg_html)
            # send_mail('Новый заказ', None, 'norply@lakshmi888.ru', ['info@lakshmi888.ru'],
            #           fail_silently=False, html_message=msg_html)
            return HttpResponseRedirect('/order/{}'.format(new_order.order_code))




        if request.POST.get('form_type') == 'checkout_guest':
            print(request.POST)
            s_key = request.session.session_key
            guest = Guest.objects.get(session=s_key)
            name = request.POST.get('name')
            family = request.POST.get('family')
            otchestvo = request.POST.get('otchestvo')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            country = request.POST.get('country')
            city = request.POST.get('city')
            post_code = request.POST.get('post_code')
            address = request.POST.get('address')
            shipping = int(request.POST.get('shipping'))
            payment = int(request.POST.get('payment'))
            with_register=request.POST.get('with_register')
            user = None
            order_code = create_password()
            register = False



            if guest.used_promo:
                promo_id = guest.used_promo.id
                print('With promo')
            else:
                promo_id = None
                print('With no promo')

            if request.POST.get('with_register') == 'on':
                print('With register')
                register = True
                password = create_password()
                user = User.objects.create_user(email=email, name=name, family=family, otchestvo=otchestvo, country=country,
                                         city=city, post_code=post_code, phone=phone, address=address, profile_ok=True,
                                         password=password)
                # msg_html = render_to_string('email/register.html', {'login': email, 'password': password})
                # send_mail('Регистрация на сайте LAKSHMI888', None, 'info@lakshmi888.ru', [email],
                #           fail_silently=False, html_message=msg_html)
            else:
                guest.email = email
                guest.name = name
                guest.family = family
                guest.otchestvo = otchestvo
                guest.country = country
                guest.city = city
                guest.post_code = post_code
                guest.phone = phone
                guest.address = address
                guest.save(force_update=True)

            if user:
                order = Order.objects.create(client=user, promo_code_id=promo_id, order_code=order_code,
                                         payment_id=int(request.POST.get('payment')),
                                         shipping_id=int(request.POST.get('shipping')))
            else:
                order = Order.objects.create(guest=guest, promo_code_id=promo_id, order_code=order_code,
                                             payment_id=int(request.POST.get('payment')),
                                             shipping_id=int(request.POST.get('shipping')))
            order.save(force_update=True)
            all_cart_items = Cart.objects.filter(guest_id=guest.id)
            for item in all_cart_items:
                ItemsInOrder.objects.create(order_id=order.id, item_id=item.item.id, number=item.number)
                item.item.item.buys = item.item.item.buys + 1
                item.item.item.save(force_update=True)
            all_cart_items.delete()




            guest.used_promo = None
            guest.save(force_update=True)
            new_order = Order.objects.get(id=order.id)
            print('total_cart_price', new_order.total_price)
            if user:
                user.bonuses += int(float(new_order.total_price_with_code) * (3 / 100))
                user.save(force_update=True)
            # msg_html = render_to_string('email/new_order.html', {'order': new_order})
            # send_mail('Заказ успешно размещен', None, 'info@lakshmi888.ru', [email],
            #           fail_silently=False, html_message=msg_html)
            # send_mail('Новый заказ', None, 'norply@lakshmi888.ru', ['info@lakshmi888.ru'],
            #           fail_silently=False, html_message=msg_html)
            print('Email sent')
            return HttpResponseRedirect('/order/{}'.format(new_order.order_code))


#-------------------------------------------------------------------------------GET request
    shipping = OrderShipping.objects.all()
    payment = OrderPayment.objects.all()

    if request.user.is_authenticated:
        client = request.user
        all_bonuses = client.bonuses
        use_bonuses = round(all_bonuses / 2)
        form = UpdateForm(instance=client)
        return render(request, 'page/checkout.html', locals())
    else:
        form = UpdateForm()
        return render(request, 'page/checkout.html', locals())




def index(request):
    show_tags = True
    title = 'Главная'
    description = ''
    keywords = ''


    all_categories = Category.objects.all()
    return render(request, 'page/index.html', locals())


def category(request, cat_slug):
    try:
        cat = Category.objects.get(name_slug=cat_slug)
        # cat.views += 1
        # cat.save()
        title = cat.page_title
        description = cat.page_description
        keywords = cat.page_keywords
        subcats = SubCategory.objects.filter(category=cat)
    except:
        raise Http404
        # return render(request, '404.html', locals())
    show_tags = True

    return render(request, 'page/catalog.html', locals())

def subcategory(request, cat_slug,subcat_slug):
   # try:
    cat = Category.objects.get(name_slug=cat_slug)
    # cat.views += 1
    # cat.save()
    title = cat.page_title
    description = cat.page_description
    keywords = cat.page_keywords
    subcategory = SubCategory.objects.get(name_slug=subcat_slug)
    subcats = SubCategory.objects.filter(name_slug=subcat_slug)
    subsubcat = subcategory.subsubcategory_set.first()
    all_items = subsubcat.item_set.filter(is_active=True)
  #  except:
   #     raise Http404
        # return render(request, '404.html', locals())
    show_tags = True

    return render(request, 'page/catalog.html', locals())


def subsubcategory(request, cat_slug,subcat_slug,subsubcat_slug):
    try:
        cat = Category.objects.get(name_slug=cat_slug)
        # cat.views += 1
        # cat.save()
        title = cat.page_title
        description = cat.page_description
        keywords = cat.page_keywords
        subcategory = SubCategory.objects.get(name_slug=subcat_slug)
        subcats = SubCategory.objects.filter(name_slug=subcat_slug)
        subsubcat = SubSubCategory.objects.get(name_slug=subsubcat_slug)
        all_items = subsubcat.item_set.filter(is_active=True)

    except:
        raise Http404
        # return render(request, '404.html', locals())
    show_tags = True

    return render(request, 'page/catalog.html', locals())

def subcategory1(request, subcat_slug):
    try:
        subcat = SubCategory.objects.get(name_slug=subcat_slug)
        all_items = Item.objects.filter(subcategory_id=subcat.id, is_active=True, is_present=True).order_by('-created_at')
        np_all_items = Item.objects.filter(subcategory_id=subcat.id, is_active=True, is_present=False)
        title = subcat.page_title
        description = subcat.page_description
        keywords = subcat.page_keywords
    except:
        raise Http404
        # return render(request, '404.html', locals())
    data = request.GET
    print(request.GET)
    search = data.get('search')
    filter = data.get('filter')
    order = data.get('order')
    count = data.get('count')
    page = request.GET.get('page')
    search_qs = None
    filter_sq = None
    np_search_qs = None
    np_filter_sq = None
    if search:
        items = all_items.filter(name_lower__contains=search.lower())
        not_present = np_all_items.filter(name_lower__contains=search.lower())

        if not items:
            items = all_items.filter(article__contains=search)
            not_present = np_all_items.filter(article__contains=search)
        search_qs = items
        np_search_qs = not_present
        param_search = search

    if filter == 'new':
        print('Поиск по фильтру туц')
        if search_qs:
            items = search_qs.filter(is_new=True)
            not_present = np_search_qs.filter(is_new=True)
            filter_sq = items
            np_filter_sq = not_present
            param_filter = filter
        else:
            items = all_items.filter(is_new=True)
            not_present = np_all_items.filter(is_new=True)
            filter_sq = items
            np_filter_sq = not_present
            param_filter = filter

        param_filter = 'new'

    if filter and filter != 'new':
        print('Поиск по фильтру')

        if search_qs:
            items = search_qs.filter(filter__name_slug=filter)
            not_present = np_search_qs.filter(filter__name_slug=filter)
            filter_sq = items
            np_filter_sq = not_present
            param_filter = filter
        else:
            items = all_items.filter(filter__name_slug=filter)
            not_present = np_all_items.filter(filter__name_slug=filter)
            filter_sq = items
            np_filter_sq = not_present
            param_filter = filter

    if order:
        if search_qs and filter_sq:
            items = filter_sq.order_by(order)
        elif filter_sq:
            items = filter_sq.order_by(order)
        elif search_qs:
            items = search_qs.order_by(order)
        else:
            items = all_items.order_by(order)
        param_order = order

    if not search and not order and not filter:
        items = all_items
        not_present = np_all_items
        # subcat.views = subcat.views + 1
        # subcat.save()
        param_order = '-created_at'

    if count:
        items_paginator = Paginator(items, int(count))
        param_count = count
    else:
        items_paginator = Paginator(items, 12)

    if page:
        canonical_link = 'https://www.lakshmi888.ru/subcategory/' + subcat.name_slug

    try:
        items = items_paginator.get_page(page)
        show_tags = False
    except PageNotAnInteger:
        items = items_paginator.page(1)
    except EmptyPage:
        items = items_paginator.page(items_paginator.num_pages)

    return render(request, 'page/subcategory.html', locals())





def search(request):
    show_tags = False
    search_string = request.GET.get('search')
    page = request.GET.get('page')
    param_search = search_string
    try:
        items = Item.objects.filter(name_lower__contains=search_string.lower(), is_active=True)
    except:
        return render(request, '404.html', locals())
    if not items:
        items = Item.objects.filter(name_lower__contains=search_string.lower()[:-1], is_active=True)
    if not items:
        items = Item.objects.filter(article__contains=search_string)
    items_paginator = Paginator(items, 12)
    try:
        items = items_paginator.get_page(page)
    except PageNotAnInteger:
        items = items_paginator.page(1)
    except EmptyPage:
        items = items_paginator.page(items_paginator.num_pages)

    return render(request, 'page/search.html', locals())


def customhandler404(request, exception, template_name='404.html'):
    response = render_to_response("404.html")
    response.status_code = 404
    return response