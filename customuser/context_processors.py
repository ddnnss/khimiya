from item.models import Category
from order.models import Wishlist
import random
def check_profile(request):
    num1 = random.randint(0, 9)
    num2 = random.randint(0, 9)
    all_cat = Category.objects.all()
    if request.user.is_authenticated:
        print('user')
        wl = Wishlist.objects.filter(client=request.user)
        wishlist_ids = []
        for i in wl:
            wishlist_ids.append(i.item.id)


    else:
        s_key = request.session.session_key
        print('guest')
        if not s_key:
            request.session.cycle_key()



    print(request.session.session_key)



    return locals()

