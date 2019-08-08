from django.db import models
from django.utils import timezone
from pytils.translit import slugify
from PIL import Image
from django.db.models.signals import post_save
import uuid
from random import choices
import string
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.utils.safestring import mark_safe
from laskshmi import settings

import os


def format_number(num):
    if num % 1 == 0:
        return int(num)
    else:
        return num

class Category(models.Model):
    name = models.CharField('Название категории', max_length=255, blank=False, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField('Изображение категории', upload_to='category_img/', blank=False)
    page_title = models.CharField('Название страницы', max_length=255, blank=False, null=True)
    page_description = models.CharField('Описание страницы', max_length=255, blank=False, null=True)
    page_keywords = models.TextField('Keywords', blank=False, null=True)
    short_description = models.TextField('Краткое описание для главной', blank=True,)
    description = RichTextUploadingField('Описание категории', blank=True, null=True)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return 'id :%s , %s ' % (self.id, self.name)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class SubCategory(models.Model):
    category = models.ForeignKey(Category, blank=False, null=True, on_delete=models.SET_NULL)
    name = models.CharField('Название подкатегории', max_length=255, blank=False, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField('Изображение подкатегории', upload_to='sub_category_img/', blank=False)
    page_title = models.CharField('Название страницы', max_length=255, blank=False, null=True)
    page_description = models.CharField('Описание страницы', max_length=255, blank=False, null=True)
    page_keywords = models.TextField('Keywords', blank=False, null=True)
    description = RichTextUploadingField('Описание подкатегории', blank=True, null=True)
    discount = models.IntegerField('Скидка на все товары в подкатегории %', blank=True, default=0)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        all_items = self.item_set.all()
        for item in all_items:
            item.discount = self.discount
            item.save()

        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return 'id :%s , %s ' % (self.id, self.name)

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"


class Filter(models.Model):
    subcategory = models.ForeignKey(SubCategory, blank=True, null=True,on_delete=models.SET_NULL, verbose_name='Подкатегория')
    name = models.CharField('Название фильтра', max_length=255, blank=False, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Filter, self).save(*args, **kwargs)

    def __str__(self):
        return '%s | %s ' % (self.subcategory.name, self.name)

    class Meta:
        verbose_name = "Фильтр"
        verbose_name_plural = "Фильтры"

class Collection(models.Model):
    category = models.ForeignKey(Category, blank=False, null=True, on_delete=models.SET_NULL, verbose_name='Категория')
    name = models.CharField('Название коллекции', max_length=255, blank=False, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField('Изображение коллекции', upload_to='collection_img/', blank=False)
    page_title = models.CharField('Название страницы', max_length=255, blank=False, null=True)
    page_description = models.TextField('Описание страницы', blank=False, null=True)
    page_keywords = models.TextField('Keywords', blank=False, null=True)
    description = RichTextUploadingField('Описание коллекции', blank=True, null=True)
    discount = models.IntegerField('Скидка на все товары в коллекции %', blank=True, default=0)
    views = models.IntegerField(default=0)
    show_at_homepage = models.BooleanField('Отображать на главной', default=True)
    show_at_category = models.BooleanField('Отображать в категории', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        all_items = Item.objects.filter(collection=self)
        for item in all_items:
            item.discount = self.discount
            item.save()
        super(Collection, self).save(*args, **kwargs)

    def __str__(self):
        return '%s ' % self.name

    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"

class Item(models.Model):
    collection = models.ManyToManyField(Collection, blank=True, verbose_name='Коллекция',db_index=True)
    filter = models.ForeignKey(Filter, blank=True, null=True, on_delete=models.SET_NULL,db_index=True)
    subcategory = models.ForeignKey(SubCategory, blank=False, null=True, verbose_name='Подкатегория', on_delete=models.SET_NULL,db_index=True)
    name = models.CharField('Название товара', max_length=255, blank=False, null=True)
    name_lower = models.CharField(max_length=255, blank=True, null=True,default='')
    name_slug = models.CharField(max_length=255, blank=True, null=True,db_index=True)
    price = models.IntegerField('Цена', blank=False, default=0, db_index=True)
    discount = models.IntegerField('Скидка %', blank=True, default=0, db_index=True)
    page_title = models.CharField('Название страницы', max_length=255, blank=False, null=True)
    page_description = models.TextField('Описание страницы',  blank=False, null=True)
    description = models.TextField('Описание товара', blank=True, null=True)
    comment = models.TextField('Комментарий', blank=True, null=True)
    length = models.CharField('Длина', max_length=15, default='не указано')
    width = models.CharField('Ширина', max_length=15, default='не указано')
    height = models.CharField('Высота',  max_length=15, default='не указано')
    article = models.CharField('Артикул', max_length=50, blank=False, null=True)
    weight = models.CharField('Вес',  max_length=15, default='не указано')
    material = models.CharField('Материал', max_length=50, blank=True, null=True, default='не указано')
    is_active = models.BooleanField('Отображать товар ?', default=True, db_index=True)
    is_present = models.BooleanField('Товар в наличии ?', default=True, db_index=True)
    is_new = models.BooleanField('Товар новинка ?', default=False, db_index=True)
    is_reserved = models.BooleanField('Товар в резерве ?', default=False)
    buys = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        self.name_lower = self.name.lower()
        super(Item, self).save(*args, **kwargs)

    def getfirstimage(self):
        url = None
        for img in self.itemimage_set.all():
            if img.is_main:
                url = img.image_small
        return url

    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        if self.getfirstimage():
            return mark_safe('<img src="{}" width="100" height="100" />'.format(self.getfirstimage()))
        else:
            return mark_safe('<span>НЕТ МИНИАТЮРЫ</span>')

    image_tag.short_description = 'Основная картинка'



    @property
    def discount_value(self):
        if self.discount > 0:
            dis_val = self.price - (self.price * self.discount / 100)
        else:
            dis_val = 0
        return (format_number(dis_val))


    def __str__(self):
        if self.filter:
            return 'id:%s %s | Фильтр %s' % (self.id, self.name, self.filter.name)
        else:
            return 'id:%s %s | Фильтра нет' % (self.id, self.name)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"



class ItemImage(models.Model):
    upload_to = 'items/%d/%s'


    def _get_upload_to(self, filename):
        ext = filename.split('.')[-1]

        filename = '{}.{}'.format(self.item.pk, ext)

        return self.upload_to % (self.item.id, filename)

    item = models.ForeignKey(Item, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Товар')
    image = models.ImageField('Изображение товара', upload_to=upload_to, blank=False)
    image_small = models.CharField(max_length=255, blank=True, default='')
    f_id = models.CharField(max_length=5, blank=True, default='')
    is_main = models.BooleanField('Основная картинка ?', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s Изображение для товара : %s ' % (self.id, self.item.name)

    class Meta:
        verbose_name = "Изображение для товара"
        verbose_name_plural = "Изображения для товара"

    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        if self.image_small:
            return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image_small))
        else:
            return mark_safe('<span>НЕТ МИНИАТЮРЫ</span>')

    image_tag.short_description = 'Картинка'


    def save(self, *args, **kwargs):
        fill_color = '#fff'
        base_image = Image.open(self.image)

        if base_image.mode in ('RGBA', 'LA'):
            background = Image.new(base_image.mode[:-1], base_image.size, fill_color)
            background.paste(base_image, base_image.split()[-1])
            base_image = background
        os.makedirs('media/items/{}'.format(self.item.id), exist_ok=True)
        watermark = Image.open('static/images/watermark30.png')
        width, height = base_image.size
        transparent = Image.new('RGB', (width, height), (0, 0, 0, 0))
        transparent.paste(base_image, (0, 0))
        transparent.paste(watermark, (291, 386), mask=watermark)
        # transparent.show()
        image_url = 'media/items/{}/{}'.format(self.item.id, str(uuid.uuid4()) + '_watermarked.jpg')
        if settings.DEBUG:
            transparent.save(image_url, 'JPEG', quality=80)
        else:
            transparent.save('laskshmi/' + image_url, 'JPEG', quality=80)
        original_image_url = 'media/items/{}/{}'.format(self.item.id, str(uuid.uuid4()) + '_original.jpg')
        if settings.DEBUG:
            base_image.save(original_image_url, 'JPEG', quality=80)
        else:
            base_image.save('laskshmi/' + original_image_url, 'JPEG', quality=80)
        # transparent.save(image_url, 'JPEG', quality=80)
        self.image = '/' + image_url


        # if image.mode in ('RGBA', 'LA'):
        #     background = Image.new(image.mode[:-1], image.size, fill_color)
        #     background.paste(image, image.split()[-1])
        #     image = background
        transparent.thumbnail((400, 400), Image.ANTIALIAS)
        small_name = 'media/items/{}/{}'.format(self.item.id, str(uuid.uuid4()) + '.jpg')
        if settings.DEBUG:
            transparent.save(small_name, 'JPEG', quality=75)
        else:
            transparent.save('laskshmi/' + small_name, 'JPEG', quality=75)
        self.image_small = '/' + small_name

        super(ItemImage, self).save(*args, **kwargs)



class PromoCode(models.Model):
    promo_code = models.CharField('Промокод (для создания рандомного значения оставить пустым)', max_length=255, blank=True, null=True)
    promo_discount = models.IntegerField('Скидка на заказ', blank=False, default=0)
    use_counts = models.IntegerField('Кол-во использований', blank=True, default=1)
    is_unlimited = models.BooleanField('Неограниченное кол-во использований', default=False)
    is_active = models.BooleanField('Активен?', default=True)
    expiry = models.DateTimeField('Срок действия безлимитного кода', default=timezone.now())

    def __str__(self):
        if self.is_unlimited:
            return 'Неограниченный промокод со скидкой : %s . Срок действия до : %s' % (self.promo_discount, self.expiry)
        else:
            return 'Ограниченный промокод со скидкой : %s . Оставшееся кол-во использований : %s' % (self.promo_discount, self.use_counts)

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"

    def save(self, *args, **kwargs):
        if self.is_unlimited:
            if not self.promo_code:
                self.promo_code = "LM-"+''.join(choices(string.ascii_uppercase + string.digits, k=5))
                self.use_counts = 0
        else:
            if not self.promo_code:
                self.promo_code = "LM-" + ''.join(choices(string.ascii_uppercase + string.digits, k=5))


        super(PromoCode, self).save(*args, **kwargs)




def ItemImage_post_save(sender,instance,**kwargs):
    base_image = Image.open(instance.image)
    fill_color = '#fff'
    os.remove(instance.image.url)
    if base_image.mode in ('RGBA', 'LA'):
        background = Image.new(base_image.mode[:-1], base_image.size, fill_color)
        background.paste(base_image, base_image.split()[-1])
        base_image = background
    watermark = Image.open('static/images/watermark.png')
    width, height = base_image.size

    transparent = Image.new('RGB', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, (0, 0), mask=watermark)
    transparent.show()
    img_path = 'media/items/{}/{}'.format(instance.item.id, str(uuid.uuid4()) + '_water.jpg')
    transparent.save(img_path, 'JPEG', quality=75)

    image = Image.open(instance.image)

    os.makedirs('media/items/{}'.format(instance.item.id), exist_ok=True)
    if image.mode in ('RGBA', 'LA'):
        background = Image.new(image.mode[:-1], image.size, fill_color)
        background.paste(image, image.split()[-1])
        image = background
    image.thumbnail((400, 400), Image.ANTIALIAS)
    small_name = 'media/items/{}/{}'.format(instance.item.id, str(uuid.uuid4()) + '.jpg')
    if settings.DEBUG:
        image.save(small_name, 'JPEG', quality=75)
    else:
        image.save('laskshmi/' + small_name, 'JPEG', quality=75)
    instance.image_small = '/' + small_name

#post_save.connect(ItemImage_post_save, sender=ItemImage)