# Generated by Django 4.2.6 on 2024-05-23 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('price_convertor', '0003_exchangerateisomodel_alter_exchangeratemodel_buy_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchangerateisomodel',
            name='currencyCodeA',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='exchangerateisomodel',
            name='currencyCodeB',
            field=models.IntegerField(),
        ),
    ]