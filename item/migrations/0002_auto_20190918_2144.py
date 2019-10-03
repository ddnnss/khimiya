# Generated by Django 2.1.5 on 2019-09-18 18:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemprice',
            options={'verbose_name': 'Объем и цену', 'verbose_name_plural': 'Объем и цену'},
        ),
        migrations.AddField(
            model_name='itemprice',
            name='unit',
            field=models.CharField(choices=[('Liter', 'Литры'), ('Unit', 'Штуки')], default='Liter', max_length=5),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 18, 18, 44, 30, 703745, tzinfo=utc), verbose_name='Срок действия безлимитного кода'),
        ),
    ]