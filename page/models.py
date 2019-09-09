from django.db import models

class Banner(models.Model):
    order = models.IntegerField('Порядок отображения', default=1)
    image = models.ImageField('Картинка', upload_to='banners/', blank=False)
    header = models.CharField('Заголовок банера', max_length=255, blank=False)
    text1 = models.CharField('Текст 1', max_length=255, blank=False)
    text2 = models.CharField('Текст 2', max_length=255, blank=False)
    is_active = models.BooleanField('Показывать?', default=True)

    def __str__(self):
        return 'Баннер, порядковый номер : %s' % self.order

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"
