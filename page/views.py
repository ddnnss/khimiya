import urllib

import requests
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

import lxml
from bs4 import BeautifulSoup
import requests as req
from urllib import request
# import xlsxwriter


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
        all_categories = Category.objects.all()
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
    discounts = ItemPrice.objects.filter(discount__gt=0)
    print(discounts)
    for x in discounts:
        print(x.item.name)


    return render(request, 'page/index.html', locals())


def category(request, cat_slug):
    try:
        cat = Category.objects.get(name_slug=cat_slug)
        # cat.views += 1
        # cat.save()
        title = cat.page_title
        description = cat.page_description
        keywords = cat.page_keywords
        all_categories = Category.objects.all()
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
    all_items = Item.objects.filter(subcategory=subsubcat.id, is_active=True)
    all_categories = Category.objects.all()
  #  except:
   #     raise Http404
        # return render(request, '404.html', locals())
    show_tags = True

    return render(request, 'page/catalog.html', locals())


def subsubcategory(request, cat_slug,subcat_slug,subsubcat_slug):
    # try:
    cat = Category.objects.get(name_slug=cat_slug)
    # cat.views += 1
    # cat.save()
    title = cat.page_title
    description = cat.page_description
    keywords = cat.page_keywords
    all_categories = Category.objects.all()
    subcategory = SubCategory.objects.get(name_slug=subcat_slug)
    subcats = SubCategory.objects.filter(name_slug=subcat_slug)
    subsubcat = SubSubCategory.objects.get(name_slug=subsubcat_slug)
    all_items = Item.objects.filter(subcategory=subsubcat.id,is_active=True)
    #https://rt.pornhub.com/view_video.php?viewkey=ph5aa51414f1112


    # except:
    #     raise Http404
    #     # return render(request, '404.html', locals())
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


def test(request):


    resp = req.get("https://specsintez.com/katalog")

    soup = BeautifulSoup(resp.text, 'lxml')
    main_structure={}
    cats=[]
    subcats={}
    print()
    for link in soup.find(id="id_1010").find_all('a'):
        if link.find('span', {'class': 'category_ids'}):
            #print(link.find('span', {'class': 'nav-label'}).text)
            # print(link.find('span',{'class':'category_ids'}))
            print(link.get('id').split('-')[1])
            if int(link.get('id').split('-')[1]) < 200 :
                print(link.find('span', {'class': 'nav-label'}).text)
                cat_id = int(link.get('id').split('-')[1])
                cat_name = (link.find('span', {'class': 'nav-label'}).text).replace('\n','').rstrip().lstrip()
                cats.append(f'{cat_id}-{cat_name}')
  #  print (cats)



    for maincat in cats:
        temp = []
        maincat = maincat.split('-')[0]
        ul = soup.find(id = f'category_{maincat}')
        subcats_items = ul.find_all('a', {'data-parent': '#id_1010'})
        for item in subcats_items:
            subcat_name = item.find_all('span', {'class': 'nav-label'})
            fullname = ''

            if len(subcat_name) > 1:
                for name in subcat_name:
                    fullname += ' ' + name.text
            else:
                fullname = subcat_name[0].text
            temp.append(item.get('id').split('-')[1])
            temp.append(fullname.replace('\n','').rstrip().lstrip())
            subcats[f'{maincat}'] = temp

 #   print(subcats)

    all_links = soup.find(id="id_1010").find_all("a", class_='start_products')

    for link in all_links:

        subsubID = link.get('id').split('-')[1]
        subcat = []
        subsubcat_name = link.find_all('span', {'class': 'nav-label'})
        fullname = ''

        if len(subsubcat_name)>1:
            for name in subsubcat_name:

                fullname += ' '+ name.text
        else:
            fullname = subsubcat_name[0].text

        temp = link.get('href').split('=')[2].replace('&path','').split('_')

        # subcat.append(fullname)
        subcat.append(f'maincat-{temp[0]}')
        subcat.append(f'subcat-{temp[1]}')

        subcat.append(f'subsubcat-{subsubID}')
        subcat.append('https://specsintez.com/' + link.get('href'))
        subcat.append(f'{subsubID} - {fullname}')

        try:
            main_structure[f'subsubcat-{temp[2]}'] = subcat
        except:
            pass

 #   print(main_structure)
    # workbook = xlsxwriter.Workbook('c:/sites/Expenses011.xlsx')
    # worksheet = workbook.add_worksheet()
    #
    # row = 0
    # col = 0
    items = []
    subsubcats=[]
    for item in main_structure:


 #       print(main_structure[item])
        resp = req.get(main_structure[item][3])
        soup = BeautifulSoup(resp.text, 'lxml')

        # itemIDS=[]
   #     print(items)
        for link in soup.find_all('div',{'class':'run_card'}):
 #           print(items)
            # print(link.find('a').get('href'))
  #          print('itemID ',link.get('id').split('-')[2])
            item_id=link.get('id').split('-')[2]
            # itemIDS.append(link.get('id').split('-')[2])
            resp = req.get('https://specsintez.com/'+link.find('a').get('href'))
            soup = BeautifulSoup(resp.text, 'lxml')
            try:
                image = soup.find(class_='thumbnail').find('img').get('src')
            except:
                image = 'картинка не спарсилось'
            # with open('c:/sites/wew.png', "wb") as f:
            #     f.write(requests.get(image).content)
            name = soup.find('h1').text
            try:
                descr = soup.find(id='tab-description').prettify(formatter="html")
            except:
                descr='описание не спарсилось'
            # print(descr)
            volumes = soup.find_all('img', {'class': 'img-thumbnail'})
            #items.append(f'{item_id},{main_structure[item][0]},{ main_structure[item][1]},{main_structure[item][2]}')
            #print(main_structure[item][4])
            if not main_structure[item][4] in subsubcats:
                subsubcats.append(main_structure[item][1])
                subsubcats.append(main_structure[item][4])
            print(subsubcats)
                # for vol in volumes:
            #     print(vol.get('alt').split(' ')[0])
            #     print(vol.get('alt').split(' ')[1])
    #         worksheet.write(row, col, link.get('id').split('-')[2])
    #         worksheet.write(row, col+1, main_structure[item][1])
    #         worksheet.write(row, col+2, main_structure[item][2])
    #         worksheet.write(row, col+3, main_structure[item][0])
    #         worksheet.write(row, col+4, name)
    #         worksheet.write(row, col+5, image)
    #         worksheet.write(row, col+6, descr)
    #         j=0
    #         for vol in volumes:
    #             worksheet.write(row, col+(7+j), vol.get('alt'))
    #             j += 1
    #         row += 1
    #
    # workbook.close()

    with open('c:/sites/subsubcats.txt', 'w') as f:
        for item in subsubcats:
            f.write("%s\n" % item)
    return





    image = soup.find(class_='thumbnail').find('img').get('src')
    # with open('c:/sites/wew.png', "wb") as f:
    #     f.write(requests.get(image).content)
    name = soup.find('h1').text
    descr = soup.find(id='tab-description').prettify( formatter="html" )
    print(descr)
    volumes = soup.find_all('img',{'class':'img-thumbnail'})
    for vol in volumes:

        print(vol.get('alt').split(' ')[0])
        print(vol.get('alt').split(' ')[1])



    worksheet.write(row, col, image)
    worksheet.write(row, col + 1, name)
    worksheet.write(row, col + 2, descr)


    workbook.close()

def test1(request):
    # a = [['65-КРС', '55-Птицеводство', '60-Свиноводство'],
    #     ['132-Дезинфекция поверхностей', '133-Обработка изделий медицинского назначения', '137-Обработка кожных покровов', '135-Обработка эндоскопов', '140-Профессиональная уборка', '1536-Стирка', '134-Дезинфекция и уборка на пищеблоке','136-Дезинфекция биологических и медицинских отходов'],
    #     ['1563-Масложировая промышленность', '1569-Молочная промышленность', '1575-Мясопереработка', '1581-Пиво и напитки', '1587-Производство соусов', '1593-Хлеб и кондитерские изделия'],
    #     ['1452-Дом', '88-Коммерческий клининг'],
    #     ['81-Гостиницы', '73-Кафе, бары, рестораны'],
    #     ['172-Гигиена кожных покровов', '1546-Дезинфекция поверхностей', '1543-Дезинфекция, совмещенная с  очисткой многоразовых  инструментов', '1553-Уборка','1552-Дезинфекция перед утилизацией ','1551-Дезинфекция уборочного инвентаря'],
    #     ['154-Гигиена кожных покровов', '157-Дезинфекция на пищеблоке', '151-Дезинфекция поверхностей', '152-Дезинфекция, совмещенная с  очисткой, многоразовых инструментов', '153-Стирка', '1445-Уборка в пищеблоке', '158-Уборка помещений','1442-Дезинфекция одноразовых инструментов и материалов перед утилизацией'],
    #     ['118-Обезжиривание поверхностей', '121-Промышленный клининг'],
    #     ['100-Категории транспорта', '95-Железнодорожный транспорт', '108-Метрополитен'],
    #     ['1478-Обслуживание коммерческой недвижимости', '1474-Производственные предприятия', '1471-Тепловые сети', '1468-Теплоэлектростанции (ТЭЦ)', '1482-Частный сектор']]
    #
    # y = 1
    # for xx in a:
    #
    #     print(xx)
    #
    #     for x in xx:
    #         subcat_id = x.split('-')[0]
    #         subcat_name = x.split('-')[1]
    #         SubCategory.objects.create(category_id=y,subcat_id=subcat_id, name=subcat_name)
    #     y+=1

    # f = open('c:/sites/subsubcats.txt')
    # for line in f:
    #     row = line.split(';')
    #     subcat_id = row[0]
    #     subsubcat_id = row[1].split('-')[0].replace(' ','')
    #     subsubcat_name = row[1].split('-')[1].lstrip()
    #     print(subcat_id,subsubcat_id, subsubcat_name)
    #     subcat = SubCategory.objects.get(subcat_id=int(subcat_id))
    #     SubSubCategory.objects.create(subcategory=subcat,name=subsubcat_name,subsubcat_id=int(subsubcat_id))
    import requests
    import shutil
    # from openpyxl import load_workbook
    # wb = load_workbook(filename='c:/sites/tovary_s_tsenami.xlsx')
    # sheet = wb.active
    # # get max row count
    # max_row = sheet.max_row
    # # get max column count
    # max_column = sheet.max_column
    # # iterate over all cells
    # # iterate over all rows
    #
    # for i in range(1, max_row + 1):
    #
    #     # iterate over all columns
    #     for j in range(1, max_column + 1):
    #         # get particular cell value
    #         print('col=', j)
    #         print(sheet.cell(row=i, column=1).value)
    #         prices=[]
    #
    #         item_id = sheet.cell(row=i, column=1).value
    #         item_name = sheet.cell(row=i, column=2).value
    #         item_descr = sheet.cell(row=i, column=4).value
    #
    #         if j==1:
    #             newitem = Item.objects.create(item_idd=int(item_id),description=item_descr,name=item_name)
    #
    #         for p in range(5, max_column + 1):
    #             print(sheet.cell(row=i, column=p).value)
    #             if sheet.cell(row=i, column=p).value:
    #                 pricee = []
    #                 price = sheet.cell(row=i, column=p).value.split('-')[1]
    #                 vol = sheet.cell(row=i, column=p).value.split('-')[0].split(' ')[0]
    #                 unit = sheet.cell(row=i, column=p).value.split('-')[0].split(' ')[1]
    #                 if unit == 'л':
    #                     unit1 = 'LITER'
    #                 else:
    #                     unit1 = 'UNIT'
    #                 ItemPrice.objects.create(item=newitem,unit=unit1,volume=vol,price=int(price))
    #                 pricee.append(vol)
    #                 pricee.append(unit)
    #                 pricee.append(price)
    #                 prices.append(pricee)
    #         if j == 1:
    #             ItemImage.objects.create(item=newitem,image='items/{}.png'.format(sheet.cell(row=i, column=1).value))
    #
    #         print(prices)

            # urllib.request.urlretrieve(sheet.cell(row=i, column=3).value.encode('utf-8'),
            #                                "c:/sites/{}.png".format(sheet.cell(row=i, column=1).value))
            # image_url = sheet.cell(row=i, column=3).value
            #
            #
            # # Open the url image, set stream to True, this will return the stream content.
            # resp = requests.get(image_url, stream=True)
            #
            # # Open a local file with wb ( write binary ) permission.
            # local_file = open("c:/sites/{}.png".format(sheet.cell(row=i, column=1).value), 'wb')
            #
            # # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            # resp.raw.decode_content = True
            #
            # # Copy the response stream raw data to local image file.
            # shutil.copyfileobj(resp.raw, local_file)
            #
            # # Remove the image url response object.
            # del resp


            # cell_obj = sheet.cell(row=i, column=j)
            # print cell value
            # print(cell_obj.value)
        # print new line
        # print('\n')

    # f = open('c:/sites/items.txt')
    # for line in f:
    #     row = line.split(',')
    #     # print(row[0],row[3].split('-')[1])
    #     subcat = SubSubCategory.objects.get(subsubcat_id=int(row[3].split('-')[1]))
    #     try:
    #         item = Item.objects.get(item_idd=int(row[0]))
    #         item.subcategory.add(subcat)
    #         item.save()
    #     except:
    #         print('notfound idd',row[0])

    pr = ItemPrice.objects.all()

    for p in pr:
        if p.unit == 'LITER':
            p.unit = 'л.'
            p.save()
        if p.unit == 'UNIT':
            p.unit = 'шт.'
            p.save()
