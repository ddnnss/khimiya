from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from item.models import PromoCode, Item


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    first_name = None
    last_name = None
    email = models.EmailField('Эл. почта', unique=True)
    is_vip = models.BooleanField('Вип?', default=False)
    name = models.CharField('Имя', max_length=50, blank=True, null=True)
    family = models.CharField('Фамилия', max_length=50, blank=True, null=True)
    otchestvo = models.CharField('Отчество', max_length=50, blank=True, null=True)
    country = models.CharField('Страна', max_length=50, blank=True, null=True)
    city = models.CharField('Город', max_length=50, blank=True, null=True)
    post_code = models.CharField('Индекс', max_length=50, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True)
    passport = models.CharField('Паспортные данные', max_length=255, blank=True, null=True)
    address = models.TextField('Адрес', blank=True, null=True)
    comment = models.TextField('Комментарий', blank=True, null=True)
    is_allow_email = models.BooleanField('Согласен на рассылку', default=True)
    used_promo = models.ForeignKey(PromoCode, blank=True, null=True, on_delete=models.SET_NULL,
                                   verbose_name='Использованный промо-код при текущей корзине')
    profile_ok = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class Guest(models.Model):
    session = models.CharField('Ключ сессии', max_length=255, blank=True, null=True)
    email = models.EmailField('Эл. почта', blank=True, null=True)
    name = models.CharField('Имя', max_length=50, blank=True, null=True)
    family = models.CharField('Фамилия', max_length=50, blank=True, null=True)
    otchestvo = models.CharField('Отчество', max_length=50, blank=True, null=True)
    country = models.CharField('Страна', max_length=50, blank=True, null=True)
    city = models.CharField('Город', max_length=50, blank=True, null=True)
    post_code = models.CharField('Индекс', max_length=50, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True)
    passport = models.CharField('Паспортные данные', max_length=255, blank=True, null=True)
    address = models.TextField('Адрес',  blank=True, null=True)
    used_promo = models.ForeignKey(PromoCode, blank=True, null=True, on_delete=models.SET_NULL,
                                   verbose_name='Использованный промо-код при текущей корзине')

    def __str__(self):
        return 'Гостевой аккаунт. EMAIL : %s' % self.email


class Review(models.Model):
    item = models.ForeignKey(Item,blank=False, on_delete=models.CASCADE,verbose_name='Отзыв о товаре')
    user = models.ForeignKey(User,blank=False, on_delete=models.CASCADE,verbose_name='Отзыв от')
    text = models.TextField('Отзыв', blank=False,default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Отзыв о товаре %s ,от %s ' % (self.item.name, self.user.email)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"