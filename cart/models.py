from django.db import models
from customuser.models import User, Guest
from item.models import ItemPrice

class Cart(models.Model):
    client = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE,
                               verbose_name='Корзина клиента')
    guest = models.ForeignKey(Guest, blank=True, null=True, default=None, on_delete=models.CASCADE,
                              verbose_name='Корзина гостя')
    item = models.ForeignKey(ItemPrice, blank=True, null=True, default=None, on_delete=models.CASCADE,
                              verbose_name='Товар')
    number = models.IntegerField('Кол-во', blank=True, null=True, default=0)
    current_price = models.IntegerField('Цена за текущий товар', default=0)
    total_price = models.IntegerField('Общая стоимость', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.client:
            return 'Товар в корзине клиента : %s ' % self.client.name
        elif self.guest:
            return 'Товар в корзине гостя : %s ' % self.guest.id
        else:
            return 'Товар в корзине'

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзинах"

    def save(self, *args, **kwargs):
        if self.item.item.discount > 0:
            self.current_price = (self.item.price - (self.item.price * self.item.item.discount / 100)) * self.number
        else:
            self.current_price = self.item.price
        self.total_price = self.number * self.current_price
        super(Cart, self).save(*args, **kwargs)
