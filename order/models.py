import decimal

from django.db import models
from django.db.models.signals import post_save, post_delete
from customuser.models import User, Guest
from item.models import Item, PromoCode
from django.utils.safestring import mark_safe

class Wishlist(models.Model):
    client = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.SET_NULL,
                               verbose_name='Клиент')
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Товар')

    def __str__(self):
        return 'Избранный товар : %s ' % self.client.email

    class Meta:
        verbose_name = "Избранный товар"
        verbose_name_plural = "Избранные товары"


class OrderStatus(models.Model):
    name = models.CharField('Статус для заказа', max_length=100, blank=False)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = "Статус для заказа"
        verbose_name_plural = "Статусы для заказов"

class OrderPayment(models.Model):
    name = models.CharField('Вариант оплаты заказа', max_length=100, blank=False)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = "Вариант оплаты заказа"
        verbose_name_plural = "Варианты оплаты заказов"

class OrderShipping(models.Model):
    name = models.CharField('Вариант доставки заказа', max_length=100, blank=False)
    deliveryCost = models.IntegerField('Стоимость доставки', default=0)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = "Вариант доставки заказа"
        verbose_name_plural = "Варианты доставки заказов"

class Order(models.Model):
    client = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE,
                               verbose_name='Заказ клиента')
    guest = models.ForeignKey(Guest, blank=True, null=True, default=None, on_delete=models.CASCADE,
                              verbose_name='Заказ гостя')
    promo_code = models.ForeignKey(PromoCode, blank=True, null=True, default=None, on_delete=models.SET_NULL,
                              verbose_name='Использованный промо-код')
    status = models.ForeignKey(OrderStatus, blank=True, null=True, default=None, on_delete=models.SET_NULL,
                              verbose_name='Статус заказа')
    payment = models.ForeignKey(OrderPayment, blank=True, null=True, default=None, on_delete=models.SET_NULL,
                               verbose_name='Оплата заказа')
    shipping = models.ForeignKey(OrderShipping, blank=True, null=True, default=None, on_delete=models.SET_NULL,
                                verbose_name='Доставка заказа')
    total_price = models.IntegerField('Общая стоимость заказа', default=0)
    total_price_with_code = models.DecimalField('Общая стоимость заказа с учетом промо-кода', decimal_places=2,
                                                max_digits=10, default=0)
    bonuses = models.DecimalField('Бонус с заказа', decimal_places=2, max_digits=6, blank=True, default=0, db_index=True)
    track_code = models.CharField('Трек код', max_length=50, blank=True, null=True)
    order_code = models.CharField('Код заказа', max_length=10, blank=True, null=True)
    is_complete = models.BooleanField('Заказ выполнен ?', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):

        if self.client:
            if self.promo_code:
                return 'Заказ № %s. Создан : %s  . Клиент: %s . Сумма заказа : %s' % (
                self.id, self.created_at.strftime('%d-%m-%Y'), self.client.email, self.total_price_with_code)
            else:
                return 'Заказ № %s. Создан : %s  . Клиент: %s . Сумма заказа : %s' % (
                self.id, self.created_at.strftime('%d-%m-%Y'), self.client.email, self.total_price)
        if self.guest:
            if self.promo_code:
                return 'Заказ № %s. Создан : %s  . Гость: %s . Сумма заказа : %s' % (
                self.id, self.created_at.strftime('%d-%m-%Y'), self.guest.email, self.total_price_with_code)
            else:
                return 'Заказ № %s. Создан : %s  . Гость: %s . Сумма заказа : %s' % (
                self.id, self.created_at.strftime('%d-%m-%Y'), self.guest.email, self.total_price)


    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def created_tag(self):

        return mark_safe('<strong>{}</strong>'.format(self.created_at.strftime('%d-%m-%Y, %H:%M:%S')))

    created_tag.short_description = mark_safe('<strong>Дaта заказа</strong>')

    def save(self, *args, **kwargs):
        if self.promo_code:
            self.total_price_with_code = self.total_price - (self.total_price * self.promo_code.promo_discount / 100)
        else:
            self.total_price_with_code = self.total_price


        super(Order, self).save(*args, **kwargs)




class ItemsInOrder(models.Model):
    order = models.ForeignKey(Order, blank=False, null=True, default=None, on_delete=models.CASCADE,
                              verbose_name='В заказе')
    item = models.ForeignKey(Item, blank=False, null=True, default=None, on_delete=models.CASCADE,
                              verbose_name='Товар')
    number = models.IntegerField('Кол-во', blank=True, null=True, default=0)
    volume = models.DecimalField('Объем', decimal_places=2,max_digits=3, blank=True, null=True, default=0)
    current_price = models.DecimalField('Цена за ед.',decimal_places=2,max_digits=10, default=0)
    total_price = models.DecimalField('Общая стоимость',decimal_places=2,max_digits=10, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.item.discount > 0:
            self.current_price = self.item.price - (self.item.price * self.item.discount / 100)
            print(self.current_price)
        else:
            self.current_price = self.item.price
        self.total_price = self.number * (decimal.Decimal(self.current_price) * self.volume)

        super(ItemsInOrder, self).save(*args, **kwargs)


    def __str__(self):
        return 'Товар : %s . В заказе № %s .' % (self.item.name, self.order.id)

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"

    def getfirstimage(self):
        url = None
        for img in self.item.itemimage_set.all():
            if img.is_main:
                url = img.image_small
        return url

    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        if self.getfirstimage():
            return mark_safe('<img src="{}" width="100" height="100" />'.format(self.getfirstimage()))
        else:
            return mark_safe('<span>НЕТ МИНИАТЮРЫ</span>')

    def name_tag(self):
        name = self.item.name
        return name

    def article_tag(self):
        name = self.item.article
        return name

    article_tag.short_description = 'Артикул'
    name_tag.short_description = 'Название товара'
    image_tag.short_description = 'Основная картинка'


def ItemsInOrder_post_save(sender,instance,**kwargs):
    try:
        order = instance.order
    except:
        order = None

    if order:
        order_total_price = 0
        all_items_in_order = ItemsInOrder.objects.filter(order=order)

        for item in all_items_in_order:
            order_total_price += item.total_price

        instance.order.total_price = order_total_price
        instance.order.save(force_update=True)


post_delete.connect(ItemsInOrder_post_save, sender=ItemsInOrder)
post_save.connect(ItemsInOrder_post_save, sender=ItemsInOrder)
