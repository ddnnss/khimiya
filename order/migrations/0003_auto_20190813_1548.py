# Generated by Django 2.1.5 on 2019-08-13 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_itemsinorder_volume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemsinorder',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Общая стоимость'),
        ),
    ]