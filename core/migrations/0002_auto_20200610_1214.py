# Generated by Django 3.0.7 on 2020-06-10 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='first_name',
            field=models.CharField(default='Jokotoye', max_length=50, verbose_name='First Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='last_name',
            field=models.CharField(default='Ademola', max_length=50, verbose_name='Last Name'),
            preserve_default=False,
        ),
    ]
